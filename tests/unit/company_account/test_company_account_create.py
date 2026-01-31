import pytest
from unittest.mock import patch
from src.company_account import CompanyAccount


class TestCompanyAccount:
    @patch("src.company_account.CompanyAccount.validate_nip_mf")
    def test_company_account_creation(self, mock_validate):
        mock_validate.return_value = True
        account = CompanyAccount("Firma", "9830920194")
        assert account.company_name == "Firma"
        assert account.nip == "9830920194"
        mock_validate.assert_called_once_with("9830920194")

    def test_nip_too_long(self):
        account = CompanyAccount("Firma", "983095742019425")
        assert account.nip == "Invalid"

    def test_nip_too_short(self):
        account = CompanyAccount("Firma", "19425")
        assert account.nip == "Invalid"

    def test_nip_empty(self):
        account = CompanyAccount("John", "")
        assert account.nip == "Invalid"

    @patch("src.company_account.CompanyAccount.validate_nip_mf")
    def test_company_account_not_registered_in_mf(self, mock_validate):
        mock_validate.return_value = False
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Firma", "1234567890")
        mock_validate.assert_called_once_with("1234567890")
