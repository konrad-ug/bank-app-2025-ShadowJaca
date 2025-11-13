from src.company_account import CompanyAccount


class TestCompanyExpressHistory:
    def test_successful_express_outgoing_registers_two_history_entries(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.balance = 1000
        assert account.try_register_outgoing_express_transfer(200) is True
        # najpierw księgowana jest kwota przelewu, potem opłata 5
        assert account.history == [-200, -5]

    def test_failed_express_outgoing_does_not_change_history(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.balance = 100
        account.history = [1]
        assert account.try_register_outgoing_express_transfer(1000) is False
        assert account.try_register_outgoing_express_transfer(-10) is False
        assert account.try_register_outgoing_express_transfer(0) is False
        assert account.history == [1]
