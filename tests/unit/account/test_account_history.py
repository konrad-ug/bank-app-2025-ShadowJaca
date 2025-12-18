import pytest
from src.account import Account


class TestAccountHistory:

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self.account = Account(0)

    def test_incoming_transfer_adds_to_history(self):
        assert self.account.try_register_incoming_transfer(100) is True
        assert self.account.balance == 100
        assert self.account.history == [100]

    def test_outgoing_transfer_adds_negative_to_history(self):
        self.account.balance = 200
        assert self.account.try_register_outgoing_transfer(50) is True
        assert self.account.balance == 150
        assert self.account.history == [-50]

    def test_failed_incoming_does_not_change_history(self):
        self.account.history = [10]
        assert self.account.try_register_incoming_transfer(0) is False
        assert self.account.history == [10]

    def test_failed_outgoing_does_not_change_history_zero_or_insufficient(self):
        self.account.balance = 20
        # zero amount
        assert self.account.try_register_outgoing_transfer(0) is False
        # insufficient balance
        assert self.account.try_register_outgoing_transfer(100) is False
        assert self.account.history == []

    def test_backward_compat_helper_register_express_transfer(self):
        # metoda pomocnicza ma tylko zwiększać saldo i zwrócić True
        assert self.account._register_express__transfer(25) is True
        assert self.account.balance == 25
        # historia nie jest modyfikowana przez metodę pomocniczą
        assert self.account.history == []
