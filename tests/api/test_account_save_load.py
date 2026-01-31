import requests
from unittest.mock import patch, MagicMock

def test_save_and_load_accounts(base_url: str):
    # 1. Tworzymy konto
    payload = {"name": "Test", "surname": "User", "pesel": "12345678901"}
    requests.post(f"{base_url}/api/accounts", json=payload, timeout=3)
    
    # 2. Mockujemy repozytorium w app.api, aby nie potrzebować działającego MongoDB
    with patch('app.api.repository') as mock_repo:
        # Przygotowujemy dane do zwrócenia przez load_all (jako obiekty PersonalAccount)
        from src.personal_account import PersonalAccount
        acc = PersonalAccount("Test", "User", "12345678901")
        acc.balance = 50
        acc.history = [50]
        mock_repo.load_all.return_value = [acc]
        
        # 3. Testujemy Save
        save_resp = requests.post(f"{base_url}/api/accounts/save", timeout=3)
        assert save_resp.status_code == 200
        assert mock_repo.save_all.called
        
        # 4. Testujemy Load
        load_resp = requests.post(f"{base_url}/api/accounts/load", timeout=3)
        assert load_resp.status_code == 200
        assert mock_repo.load_all.called
        
        # 5. Sprawdzamy czy konto zostało załadowane do rejestru
        get_resp = requests.get(f"{base_url}/api/accounts/12345678901", timeout=3)
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["pesel"] == "12345678901"
