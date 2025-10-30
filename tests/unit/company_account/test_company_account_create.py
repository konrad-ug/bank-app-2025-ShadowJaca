from src.company_account import CompanyAccount


class TestCompanyAccount:
    def test_company_account_creation(self):
        account = CompanyAccount("Firma","9830920194")
        assert account.company_name == "Firma"
        assert account.nip == "9830920194"


    def test_nip_too_long(self):
        account = CompanyAccount("Firma","983095742019425")
        assert account.nip == "Invalid"

    def test_nip_too_short(self):
        account = CompanyAccount("Firma","19425")
        assert account.nip == "Invalid"

    def test_nip_empty(self):
        account = CompanyAccount("John", "")
        assert account.nip == "Invalid"
