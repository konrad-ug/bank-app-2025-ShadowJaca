from src.personal_account import PersonalAccount


class TestPersonalExpressHistory:
    def test_successful_express_outgoing_registers_two_history_entries(self):
        account = PersonalAccount("John", "Doe", "98309201942")
        account.balance = 200
        assert account.try_register_outgoing_express_transfer(50) is True
        # najpierw księgowana jest kwota przelewu, potem opłata
        assert account.history == [-50, -1]

    def test_failed_express_outgoing_does_not_change_history(self):
        account = PersonalAccount("John", "Doe", "98309201942")
        account.balance = 40
        account.history = [10]
        # próba większej kwoty niż saldo
        assert account.try_register_outgoing_express_transfer(100) is False
        # próba kwoty ujemnej
        assert account.try_register_outgoing_express_transfer(-10) is False
        # próba kwoty zero
        assert account.try_register_outgoing_express_transfer(0) is False
        # historia bez zmian
        assert account.history == [10]
