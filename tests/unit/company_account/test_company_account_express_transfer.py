import pytest

from src.company_account import CompanyAccount


class TestCompanyExpressTransfer:

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self.account = CompanyAccount("Tech Corp", "1234567890")



    def test_outgoing_express_transfer_zero(self):
        balance = 1000
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(0) == False
        assert self.account.balance == balance

    def test_outgoing_express_transfer_insufficient_balance_positive_amount(self):
        balance = 500
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(1000) == False
        assert self.account.balance == balance

    def test_outgoing_express_transfer_negative_amount(self):
        balance = 500
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(-100) == False
        assert self.account.balance == balance

    def test_outgoing_express_transfer_sufficient_balance_positive_amount(self):
        transfer_fee = 5
        balance = 1000
        transfer_amount = 500
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(transfer_amount) == True
        assert self.account.balance == balance - transfer_amount - transfer_fee

    def test_outgoing_express_transfer_with_exact_balance(self):
        transfer_fee = 5
        balance = 500
        transfer_amount = 500
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(transfer_amount) == True
        assert self.account.balance == balance - transfer_amount - transfer_fee

    def test_outgoing_express_transfer_large_amount(self):
        transfer_fee = 5
        balance = 100000
        transfer_amount = 75000
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(transfer_amount) == True
        assert self.account.balance == balance - transfer_amount - transfer_fee