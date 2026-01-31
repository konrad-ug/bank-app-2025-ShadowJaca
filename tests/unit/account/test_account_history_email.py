import pytest
from unittest.mock import patch
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from datetime import date

class TestAccountHistoryEmail:

    @pytest.fixture(autouse=True)
    def setup_accounts(self):
        self.personal_account = PersonalAccount("Jan", "Kowalski", "61010112345")
        self.personal_account.history = [100, -1, 500]
        
        with patch('src.company_account.CompanyAccount.validate_nip_mf', return_value=True):
            self.company_account = CompanyAccount("Firma", "1234567890")
        self.company_account.history = [5000, -1000, 500]

    @patch('src.smtp.smtp.SMTPClient.send')
    def test_send_history_via_email_personal_account_success(self, mock_send):
        mock_send.return_value = True
        recipient = "test@example.com"
        today = date.today().strftime("%Y-%m-%d")
        
        result = self.personal_account.send_history_via_email(recipient)
        
        assert result is True
        expected_subject = f"Account Transfer History {today}"
        expected_text = "Personal account history: [100, -1, 500]"
        mock_send.assert_called_once_with(expected_subject, expected_text, recipient)

    @patch('src.smtp.smtp.SMTPClient.send')
    def test_send_history_via_email_personal_account_failure(self, mock_send):
        mock_send.return_value = False
        recipient = "test@example.com"
        
        result = self.personal_account.send_history_via_email(recipient)
        
        assert result is False

    @patch('src.smtp.smtp.SMTPClient.send')
    def test_send_history_via_email_company_account_success(self, mock_send):
        mock_send.return_value = True
        recipient = "biznes@firma.pl"
        today = date.today().strftime("%Y-%m-%d")
        
        result = self.company_account.send_history_via_email(recipient)
        
        assert result is True
        expected_subject = f"Account Transfer History {today}"
        expected_text = "Company account history: [5000, -1000, 500]"
        mock_send.assert_called_once_with(expected_subject, expected_text, recipient)
