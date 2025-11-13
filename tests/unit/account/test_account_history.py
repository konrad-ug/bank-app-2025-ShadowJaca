from src.account import Account


class TestAccountHistory:
    def test_incoming_transfer_adds_to_history(self):
        account = Account(0)
        assert account.try_register_incoming_transfer(100) is True
        assert account.balance == 100
        assert account.history == [100]

    def test_outgoing_transfer_adds_negative_to_history(self):
        account = Account(0)
        account.balance = 200
        assert account.try_register_outgoing_transfer(50) is True
        assert account.balance == 150
        assert account.history == [-50]

    def test_failed_incoming_does_not_change_history(self):
        account = Account(0)
        account.history = [10]
        assert account.try_register_incoming_transfer(0) is False
        assert account.history == [10]

    def test_failed_outgoing_does_not_change_history_zero_or_insufficient(self):
        account = Account(0)
        account.balance = 20
        # zero amount
        assert account.try_register_outgoing_transfer(0) is False
        # insufficient balance
        assert account.try_register_outgoing_transfer(100) is False
        assert account.history == []

    def test_backward_compat_helper_register_express_transfer(self):
        account = Account(0)
        # metoda pomocnicza ma tylko zwiększać saldo i zwrócić True
        assert account._register_express__transfer(25) is True
        assert account.balance == 25
        # historia nie jest modyfikowana przez metodę pomocniczą
        assert account.history == []
