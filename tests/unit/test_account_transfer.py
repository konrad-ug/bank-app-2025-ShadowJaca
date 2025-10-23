from src.account import Account


class TestAccount:
    def test_outgoing_transfer_zero(self):
        account = Account("John", "Doe", "98309201942")
        balance = 100
        account.balance = balance
        assert account.try_register_outgoing_transfer(0) == False
        assert account.balance == balance

    def test_outgoing_transfer_insufficient_balance_positive_amount(self):
        account = Account("John", "Doe", "98309201942")
        balance = 50
        account.balance = balance
        assert account.try_register_outgoing_transfer(100) == False
        assert account.balance == balance

    def test_outgoing_transfer_negative_amount(self):
        account = Account("John", "Doe", "98309201942")
        balance = 50
        account.balance = balance
        assert account.try_register_outgoing_transfer(-100) == False
        assert account.balance == balance

    def test_outgoing_transfer_sufficient_balance_positive_amount(self):
        account = Account("John", "Doe", "98309201942")
        balance = 100
        transfer_amount = 50
        account.balance = balance
        assert account.try_register_outgoing_transfer(transfer_amount) == True
        assert account.balance == balance - transfer_amount

    def test_ingoing_transfer_zero(self):
        account = Account("John", "Doe", "98309201942")
        balance = 100
        account.balance = balance
        assert account.try_register_incoming_transfer(0) == False
        assert account.balance == balance

    def test_ingoing_transfer_positive_amount(self):
        account = Account("John", "Doe", "98309201942")
        balance = 100
        transfer_amount = 50
        account.balance = balance
        assert account.try_register_incoming_transfer(transfer_amount) == True
        assert account.balance == balance + transfer_amount

    def test_ingoing_transfer_negative_amount(self):
        account = Account("John", "Doe", "98309201942")
        balance = 100
        transfer_amount = -50
        account.balance = balance
        assert account.try_register_incoming_transfer(transfer_amount) == False
        assert account.balance == balance
