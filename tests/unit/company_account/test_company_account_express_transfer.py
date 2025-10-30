from src.company_account import CompanyAccount


class TestCompanyExpressTransfer:
    def test_outgoing_express_transfer_zero(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        balance = 1000
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(0) == False
        assert account.balance == balance

    def test_outgoing_express_transfer_insufficient_balance_positive_amount(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        balance = 500
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(1000) == False
        assert account.balance == balance

    def test_outgoing_express_transfer_negative_amount(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        balance = 500
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(-100) == False
        assert account.balance == balance

    def test_outgoing_express_transfer_sufficient_balance_positive_amount(self):
        transfer_fee = 5
        account = CompanyAccount("Tech Corp", "1234567890")
        balance = 1000
        transfer_amount = 500
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(transfer_amount) == True
        assert account.balance == balance - transfer_amount - transfer_fee

    def test_outgoing_express_transfer_with_exact_balance(self):
        transfer_fee = 5
        account = CompanyAccount("Tech Corp", "1234567890")
        balance = 500
        transfer_amount = 500
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(transfer_amount) == True
        assert account.balance == balance - transfer_amount - transfer_fee

    def test_outgoing_express_transfer_large_amount(self):
        transfer_fee = 5
        account = CompanyAccount("Tech Corp", "1234567890")
        balance = 100000
        transfer_amount = 75000
        account.balance = balance
        assert account.try_register_outgoing_express_transfer(transfer_amount) == True
        assert account.balance == balance - transfer_amount - 1