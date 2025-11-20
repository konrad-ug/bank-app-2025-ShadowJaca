import pytest

from src.personal_account import PersonalAccount


class TestPersonalExpressHistory:

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self.account = PersonalAccount("Jane", "Doe", "98309201942")

    def test_successful_express_outgoing_registers_two_history_entries(self):
        self.account.balance = 200
        assert self.account.try_register_outgoing_express_transfer(50) is True
        # najpierw księgowana jest kwota przelewu, potem opłata
        assert self.account.history == [-50, -1]

    def test_failed_express_outgoing_does_not_change_history(self):
        self.account.balance = 40
        self.account.history = [10]
        # próba większej kwoty niż saldo
        assert self.account.try_register_outgoing_express_transfer(100) is False
        # próba kwoty ujemnej
        assert self.account.try_register_outgoing_express_transfer(-10) is False
        # próba kwoty zero
        assert self.account.try_register_outgoing_express_transfer(0) is False
        # historia bez zmian
        assert self.account.history == [10]
