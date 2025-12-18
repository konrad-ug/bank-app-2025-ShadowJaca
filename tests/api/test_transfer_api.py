import pytest
import requests


def _create_account(base_url: str, name: str, surname: str, pesel: str, promo_code=None):
    payload = {"name": name, "surname": surname, "pesel": pesel}
    if promo_code is not None:
        payload["promo_code"] = promo_code
    return requests.post(f"{base_url}/api/accounts", json=payload, timeout=3)


@pytest.mark.parametrize(
    "transfer_type,amount,expected_status,desc",
    [
        ("incoming", 500, 200, "incoming ok"),
        ("outgoing", 60, 200, "outgoing with sufficient balance"),
        ("express", 40, 200, "express with sufficient balance"),
    ],
)
def test_transfer_happy_paths(base_url: str, transfer_type: str, amount: int, expected_status: int, desc: str):
    # given
    pesel = "90010122222"
    r = _create_account(base_url, "John", "Doe", pesel)
    assert r.status_code == 201

    # seed balance for outgoing/express
    seed = 200
    seed_resp = requests.post(
        f"{base_url}/api/accounts/{pesel}/transfer",
        json={"amount": seed, "type": "incoming"},
        timeout=3,
    )
    assert seed_resp.status_code == 200

    # when
    resp = requests.post(
        f"{base_url}/api/accounts/{pesel}/transfer",
        json={"amount": amount, "type": transfer_type},
        timeout=3,
    )

    # then
    assert resp.status_code == expected_status
    body = resp.json()
    assert isinstance(body, dict)
    if expected_status == 200:
        assert body.get("message") == "Zlecenie przyjęto do realizacji"

    # and balance reflects operation
    acc_resp = requests.get(f"{base_url}/api/accounts/{pesel}", timeout=3)
    assert acc_resp.status_code == 200
    acc = acc_resp.json()

    if transfer_type == "incoming":
        assert acc["balance"] == seed + amount
    elif transfer_type == "outgoing":
        assert acc["balance"] == seed - amount
    elif transfer_type == "express":
        # fee = 1
        assert acc["balance"] == seed - amount - 1


def test_transfer_returns_404_when_account_not_found(base_url: str):
    resp = requests.post(
        f"{base_url}/api/accounts/00000000000/transfer",
        json={"amount": 100, "type": "incoming"},
        timeout=3,
    )
    assert resp.status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"type": "incoming"},  # missing amount
        {"amount": 100},  # missing type
        {"amount": 0, "type": "incoming"},  # non-positive amount
        {"amount": -50, "type": "outgoing"},  # non-positive amount
        {"amount": "xyz", "type": "incoming"},  # wrong amount type
    ],
)
def test_transfer_bad_request_on_invalid_payload(base_url: str, payload):
    pesel = "81010133333"
    assert _create_account(base_url, "Jane", "Smith", pesel).status_code == 201

    resp = requests.post(
        f"{base_url}/api/accounts/{pesel}/transfer",
        json=payload,
        timeout=3,
    )
    assert resp.status_code == 400
    data = resp.json()
    assert isinstance(data, dict)
    assert "error" in data


def test_outgoing_returns_422_when_insufficient_funds(base_url: str):
    pesel = "70010144444"
    assert _create_account(base_url, "Alice", "Cooper", pesel).status_code == 201

    resp = requests.post(
        f"{base_url}/api/accounts/{pesel}/transfer",
        json={"amount": 100, "type": "outgoing"},
        timeout=3,
    )
    assert resp.status_code == 422
    # balance should remain 0
    acc = requests.get(f"{base_url}/api/accounts/{pesel}", timeout=3).json()
    assert acc["balance"] == 0


def test_unknown_transfer_type_returns_400(base_url: str):
    pesel = "72020255555"
    assert _create_account(base_url, "Bob", "Marley", pesel).status_code == 201

    resp = requests.post(
        f"{base_url}/api/accounts/{pesel}/transfer",
        json={"amount": 50, "type": "mysterious"},
        timeout=3,
    )
    assert resp.status_code == 400
    data = resp.json()
    assert data.get("error")
