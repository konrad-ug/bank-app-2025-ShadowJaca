import pytest
import requests

def test_performance_create_delete_100_times(base_url: str):
    for i in range(100):
        pesel = f"000000{i:05d}"
        payload = {"name": "Jan", "surname": "Kowalski", "pesel": pesel}
        
        create_resp = requests.post(f"{base_url}/api/accounts", json=payload, timeout=0.5)
        assert create_resp.status_code == 201
        
        delete_resp = requests.delete(f"{base_url}/api/accounts/{pesel}", timeout=0.5)
        assert delete_resp.status_code == 200

def test_performance_100_incoming_transfers(base_url: str):
    pesel = "12345678901"
    payload = {"name": "Jan", "surname": "Kowalski", "pesel": pesel}
    create_resp = requests.post(f"{base_url}/api/accounts", json=payload, timeout=0.5)
    assert create_resp.status_code == 201

    for _ in range(100):
        transfer_payload = {"amount": 100, "type": "incoming"}
        transfer_resp = requests.post(f"{base_url}/api/accounts/{pesel}/transfer", json=transfer_payload, timeout=0.5)
        assert transfer_resp.status_code == 200

    get_resp = requests.get(f"{base_url}/api/accounts/{pesel}", timeout=0.5)
    assert get_resp.status_code == 200
    assert get_resp.json()["balance"] == 10000

def test_performance_create_1000_then_delete_all(base_url: str):
    pesels = [f"100000{i:05d}" for i in range(1000)]
    
    for pesel in pesels:
        payload = {"name": "Jan", "surname": "Kowalski", "pesel": pesel}
        create_resp = requests.post(f"{base_url}/api/accounts", json=payload, timeout=0.5)
        assert create_resp.status_code == 201

    for pesel in pesels:
        delete_resp = requests.delete(f"{base_url}/api/accounts/{pesel}", timeout=0.5)
        assert delete_resp.status_code == 200
