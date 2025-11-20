import pytest
from src.account import Account


class TestTransfer:
    
    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self.account = Account(0)
        
        
    def test_outgoing_transfer_zero(self):
        balance = 100
        self.account.balance = balance
        assert self.account.try_register_outgoing_transfer(0) == False
        assert self.account.balance == balance

    def test_outgoing_transfer_insufficient_balance_positive_amount(self):
        balance = 50
        self.account.balance = balance
        assert self.account.try_register_outgoing_transfer(100) == False
        assert self.account.balance == balance

    def test_outgoing_transfer_negative_amount(self):
        balance = 50
        self.account.balance = balance
        assert self.account.try_register_outgoing_transfer(-100) == False
        assert self.account.balance == balance

    def test_outgoing_transfer_sufficient_balance_positive_amount(self):
        balance = 100
        transfer_amount = 50
        self.account.balance = balance
        assert self.account.try_register_outgoing_transfer(transfer_amount) == True
        assert self.account.balance == balance - transfer_amount

    def test_ingoing_transfer_zero(self):
        balance = 100
        self.account.balance = balance
        assert self.account.try_register_incoming_transfer(0) == False
        assert self.account.balance == balance

    def test_ingoing_transfer_positive_amount(self):
        balance = 100
        transfer_amount = 50
        self.account.balance = balance
        assert self.account.try_register_incoming_transfer(transfer_amount) == True
        assert self.account.balance == balance + transfer_amount

    def test_ingoing_transfer_negative_amount(self):
        balance = 100
        transfer_amount = -50
        self.account.balance = balance
        assert self.account.try_register_incoming_transfer(transfer_amount) == False
        assert self.account.balance == balance

    def account(self, param):
        pass
