import requests


def _create_account(base_url: str, name: str, surname: str, pesel: str, promo_code=None):
    payload = {"name": name, "surname": surname, "pesel": pesel}
    if promo_code is not None:
        payload["promo_code"] = promo_code
    return requests.post(f"{base_url}/api/accounts", json=payload, timeout=3)


def test_create_account_and_list(base_url: str):
    # when
    r = _create_account(base_url, "James", "Hetfield", "90010112345")

    # then
    assert r.status_code == 201
    list_resp = requests.get(f"{base_url}/api/accounts", timeout=3)
    assert list_resp.status_code == 200
    accounts = list_resp.json()
    assert isinstance(accounts, list)
    assert any(a["pesel"] == "90010112345" for a in accounts)


def test_get_account_by_pesel(base_url: str):
    _create_account(base_url, "Lars", "Ulrich", "81020298765")

    resp = requests.get(f"{base_url}/api/accounts/81020298765", timeout=3)
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Lars"
    assert data["surname"] == "Ulrich"
    assert data["pesel"] == "81020298765"
    assert "balance" in data


def test_get_account_by_pesel_not_found_returns_404(base_url: str):
    resp = requests.get(f"{base_url}/api/accounts/00000000000", timeout=3)
    assert resp.status_code == 404


def test_patch_updates_only_provided_fields(base_url: str):
    _create_account(base_url, "Dave", "Mustaine", "70030311223")

    # update tylko imię
    patch_resp = requests.patch(
        f"{base_url}/api/accounts/70030311223",
        json={"name": "David"},
        timeout=3,
    )
    assert patch_resp.status_code == 200
    acc_after = requests.get(f"{base_url}/api/accounts/70030311223", timeout=3).json()
    assert acc_after["name"] == "David"
    assert acc_after["surname"] == "Mustaine"  # niezmienione

    # update tylko nazwisko
    patch_resp2 = requests.patch(
        f"{base_url}/api/accounts/70030311223",
        json={"surname": "Ellefson"},
        timeout=3,
    )
    assert patch_resp2.status_code == 200
    acc_after2 = requests.get(f"{base_url}/api/accounts/70030311223", timeout=3).json()
    assert acc_after2["name"] == "David"
    assert acc_after2["surname"] == "Ellefson"


def test_delete_account(base_url: str):
    _create_account(base_url, "Kirk", "Hammett", "72040455667")

    del_resp = requests.delete(f"{base_url}/api/accounts/72040455667", timeout=3)
    assert del_resp.status_code == 200

    # Should be gone now
    get_resp = requests.get(f"{base_url}/api/accounts/72040455667", timeout=3)
    assert get_resp.status_code == 404


def test_count_endpoint(base_url: str):
    # 0 na starcie zapewnia fixture cleanup_registry
    c0 = requests.get(f"{base_url}/api/accounts/count", timeout=3).json()["count"]
    assert c0 == 0

    _create_account(base_url, "James", "Hetfield", "90120112345")
    _create_account(base_url, "Lars", "Ulrich", "80120198765")

    c2 = requests.get(f"{base_url}/api/accounts/count", timeout=3).json()["count"]
    assert c2 == 2
