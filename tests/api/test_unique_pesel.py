import requests


def _create_account(base_url: str, name: str, surname: str, pesel: str, promo_code=None):
    payload = {"name": name, "surname": surname, "pesel": pesel}
    if promo_code is not None:
        payload["promo_code"] = promo_code
    return requests.post(f"{base_url}/api/accounts", json=payload, timeout=3)


def test_duplicate_pesel_returns_409_and_message(base_url: str):
    pesel = "90010111111"

    # first creation ok
    r1 = _create_account(base_url, "John", "Doe", pesel)
    assert r1.status_code == 201

    # duplicate should be rejected
    r2 = _create_account(base_url, "Jane", "Smith", pesel)
    assert r2.status_code == 409

    data = r2.json()
    assert isinstance(data, dict)
    assert data.get("error") == "Account with this PESEL already exists"

    # ensure only one account with this PESEL exists
    list_resp = requests.get(f"{base_url}/api/accounts", timeout=3)
    assert list_resp.status_code == 200
    accounts = [a for a in list_resp.json() if a.get("pesel") == pesel]
    assert len(accounts) == 1
