import pytest

from src.company_account import CompanyAccount


class TestCompanyExpressHistory:

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self.account = CompanyAccount("Tech Corp", "1234567890")

    def test_successful_express_outgoing_registers_two_history_entries(self):
        self.account = CompanyAccount("Tech Corp", "1234567890")
        self.account.balance = 1000
        assert self.account.try_register_outgoing_express_transfer(200) is True
        # najpierw księgowana jest kwota przelewu, potem opłata 5
        assert self.account.history == [-200, -5]

    def test_failed_express_outgoing_does_not_change_history(self):
        self.account = CompanyAccount("Tech Corp", "1234567890")
        self.account.balance = 100
        self.account.history = [1]
        assert self.account.try_register_outgoing_express_transfer(1000) is False
        assert self.account.try_register_outgoing_express_transfer(-10) is False
        assert self.account.try_register_outgoing_express_transfer(0) is False
        assert self.account.history == [1]
