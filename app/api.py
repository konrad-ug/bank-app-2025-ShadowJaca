from flask import Flask, request, jsonify

from src.accounts_registry import AccountsRegistry
from src.personal_account import PersonalAccount
from src.mongo_accounts_repository import MongoAccountsRepository


app = Flask(__name__)
registry = AccountsRegistry()
repository = MongoAccountsRepository()


def serialize_account(acc: PersonalAccount) -> dict:
    return {
        "name": acc.first_name,
        "surname": acc.last_name,
        "pesel": acc.pesel,
        "balance": acc.balance,
    }


def _find_account_id_by_pesel(pesel: str):
    acc = registry.get_by_pesel(pesel)
    if acc is None:
        return None
    # Szukamy id po referencji obiektu (bez korzystania z prywatnych map)
    for acc_id, obj in registry._by_id.items():  # noqa: SLF001 (świadomie używamy do wyszukania id)
        if obj is acc:
            return acc_id
    return None


@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.get_json(silent=True) or {}
    if not {"name", "surname", "pesel"}.issubset(data.keys()):
        return jsonify({"error": "Missing required fields: name, surname, pesel"}), 400

    try:
        registry.add_personal_account(
            first_name=data["name"],
            last_name=data["surname"],
            pesel=data["pesel"],
            promo_code=data.get("promo_code"),
        )
    except ValueError as ex:  # mapujemy komunikaty do kodów HTTP
        msg = str(ex)
        if "invalid" in msg.lower():
            return jsonify({"error": "PESEL invalid"}), 400
        if "already exists" in msg.lower():
            return jsonify({"error": "Account with this PESEL already exists"}), 409
        return jsonify({"error": msg}), 400

    return jsonify({"message": "Account created"}), 201


@app.route("/api/accounts", methods=["GET"])
def get_all_accounts():
    accounts = registry.list_all()
    return jsonify([serialize_account(a) for a in accounts]), 200


@app.route("/api/accounts/count", methods=["GET"])
def get_account_count():
    count = len(registry.list_all())
    return jsonify({"count": count}), 200


@app.route("/api/accounts/<pesel>", methods=["GET"])
def get_account_by_pesel(pesel):
    acc = registry.get_by_pesel(pesel)
    if acc is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify(serialize_account(acc)), 200


@app.route("/api/accounts/<pesel>", methods=["PATCH"])
def update_account(pesel):
    acc = registry.get_by_pesel(pesel)
    if acc is None:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json(silent=True) or {}
    disallowed = set(data.keys()) - {"name", "surname"}
    if disallowed:
        return (
            jsonify({"error": "Only 'name' and 'surname' can be updated"}),
            400,
        )

    if "name" in data:
        acc.first_name = data["name"]
    if "surname" in data:
        acc.last_name = data["surname"]

    return jsonify({"message": "Account updated", "account": serialize_account(acc)}), 200


@app.route("/api/accounts/<pesel>", methods=["DELETE"])
def delete_account(pesel):
    acc_id = _find_account_id_by_pesel(pesel)
    if acc_id is None:
        return jsonify({"error": "Account not found"}), 404

    registry.remove(acc_id)
    return jsonify({"message": "Account deleted"}), 200


@app.route("/api/accounts/<pesel>/transfer", methods=["POST"])
def register_transfer(pesel: str):
    acc = registry.get_by_pesel(pesel)
    if acc is None:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json(silent=True) or {}
    if not {"amount", "type"}.issubset(data.keys()):
        return jsonify({"error": "Missing required fields: amount, type"}), 400

    amount = data.get("amount")
    ttype = data.get("type")

    # Walidacja amount
    try:
        amount = float(amount)
    except Exception:
        return jsonify({"error": "Field 'amount' must be a number"}), 400
    if amount <= 0:
        return jsonify({"error": "Field 'amount' must be > 0"}), 400

    if ttype not in {"incoming", "outgoing", "express"}:
        return jsonify({"error": "Unknown transfer type"}), 400

    ok = False
    if ttype == "incoming":
        ok = acc.try_register_incoming_transfer(amount)
        if not ok:
            return jsonify({"error": "Transfer failed"}), 400
    elif ttype == "outgoing":
        ok = acc.try_register_outgoing_transfer(amount)
        if not ok:
            return jsonify({"error": "Transfer could not be processed"}), 422
    elif ttype == "express":
        method = getattr(acc, "try_register_outgoing_express_transfer", None)
        if method is None:
            return jsonify({"error": "Express transfer not supported"}), 400
        ok = method(amount)
        if not ok:
            return jsonify({"error": "Transfer could not be processed"}), 422

    return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200


@app.route("/api/accounts/save", methods=["POST"])
def save_accounts():
    accounts = registry.list_all()
    repository.save_all(accounts)
    return jsonify({"message": "Accounts saved"}), 200


@app.route("/api/accounts/load", methods=["POST"])
def load_accounts():
    accounts = repository.load_all()
    registry.clear()
    for acc in accounts:
        registry.add_personal_account(
            acc.first_name,
            acc.last_name,
            acc.pesel
        )
        new_acc = registry.get_by_pesel(acc.pesel)
        if new_acc:
            new_acc.balance = acc.balance
            new_acc.history = acc.history
    return jsonify({"message": "Accounts loaded"}), 200


if __name__ == "__main__":
    # Lokalny start (np. `python app\api.py`) – przy testach korzystamy z `flask --app ... run`
    app.run(debug=True)
