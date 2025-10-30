from src.personal_account import PersonalAccount


class TestExpressTransfer:
    def test_outgoing_express_transfer_zero(self):
        account = PersonalAccount("John", "Doe", "98309201942")
        balance = 100
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(0) == False
        assert account.balance == balance

    def test_outgoing_express_transfer_insufficient_balance_positive_amount(self):
        account = PersonalAccount("John", "Doe", "98309201942")
        balance = 50
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(100) == False
        assert account.balance == balance

    def test_outgoing_express_transfer_negative_amount(self):
        account = PersonalAccount("John", "Doe", "98309201942")
        balance = 50
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(-100) == False
        assert account.balance == balance

    def test_outgoing_express_transfer_sufficient_balance_positive_amount(self):
        transfer_fee = 1
        account = PersonalAccount("John", "Doe", "98309201942")
        balance = 100
        transfer_amount = 50
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(transfer_amount) == True
        assert account.balance == balance - transfer_amount - transfer_fee

    def test_outgoing_express_transfer_with_exact_balance(self):
        transfer_fee = 1
        account = PersonalAccount("John", "Doe", "98309201942")
        balance = 50
        transfer_amount = 50
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(transfer_amount) == True
        assert account.balance == balance - transfer_amount - transfer_fee