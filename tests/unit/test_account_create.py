from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "98309201942")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "98309201942"

    def test_pesel_too_long(self):
        account = Account("John", "Doe", "983092034631974")
        assert account.pesel == "Invalid"

    def test_pesel_too_short(self):
        account = Account("John", "Doe", "92019")
        assert account.pesel == "Invalid"

    def test_pesel_empty(self):
        account = Account("John", "Doe", "")
        assert account.pesel == "Invalid"