from flask import Flask, request, jsonify

from src.accounts_registry import AccountsRegistry
from src.personal_account import PersonalAccount


app = Flask(__name__)
registry = AccountsRegistry()


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


if __name__ == "__main__":
    # Lokalny start (np. `python app\api.py`) – przy testach korzystamy z `flask --app ... run`
    app.run(debug=True)
