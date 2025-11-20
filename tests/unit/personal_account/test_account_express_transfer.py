import pytest
from src.personal_account import PersonalAccount


class TestExpressTransfer:

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self.account = PersonalAccount("Jane", "Doe", "98309201942")

    def test_outgoing_express_transfer_zero(self):
        balance = 100
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(0) == False
        assert self.account.balance == balance

    def test_outgoing_express_transfer_insufficient_balance_positive_amount(self):
        balance = 50
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(100) == False
        assert self.account.balance == balance

    def test_outgoing_express_transfer_negative_amount(self):
        balance = 50
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(-100) == False
        assert self.account.balance == balance

    def test_outgoing_express_transfer_sufficient_balance_positive_amount(self):
        transfer_fee = 1
        balance = 100
        transfer_amount = 50
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(transfer_amount) == True
        assert self.account.balance == balance - transfer_amount - transfer_fee

    def test_outgoing_express_transfer_with_exact_balance(self):
        transfer_fee = 1
        balance = 50
        transfer_amount = 50
        self.account.balance = balance
        assert self.account.try_register_outgoing_express_transfer(transfer_amount) == True
        assert self.account.balance == balance - transfer_amount - transfer_fee