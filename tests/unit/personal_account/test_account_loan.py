import pytest

from src.personal_account import PersonalAccount


class TestPersonalAccountLoan:

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self.account = PersonalAccount("Jane", "Doe", "98309201942")
    def test_loan_granted_when_last_three_are_deposits(self):
        self.account.history = [10, -5, 20, 30, 40]  # ostatnie trzy: 20, 30, 40 (wszystkie dodatnie)
        self.account.balance = 100

        amount = 500
        assert self.account.submit_for_loan(amount) is True
        assert self.account.balance == 100 + amount

    def test_loan_granted_when_sum_of_last_five_greater_than_amount(self):
        # Ostatnie trzy nie są wszystkimi wpłatami, ale suma pięciu ostatnich > amount
        self.account.history = [100, -50, 20, -10, 5]
        self.account.balance = 0

        amount = 60  # suma ostatnich 5 = 65 > 60
        assert self.account.submit_for_loan(amount) is True
        assert self.account.balance == amount

    def test_loan_denied_when_not_enough_history_and_last_three_not_all_deposits(self):
        self.account.history = [10, -1]  # mniej niż 3 i mniej niż 5 transakcji
        self.account.balance = 0

        assert self.account.submit_for_loan(100) is False
        assert self.account.balance == 0

    def test_loan_denied_when_sum_of_last_five_equal_to_amount(self):
        # suma ostatnich pięciu = 50, ostatnie trzy nie są wszystkimi wpłatami
        self.account.history = [10, -5, 20, -10, 35]
        self.account.balance = 0

        assert self.account.submit_for_loan(50) is False  # wymagane: ściśle większa
        assert self.account.balance == 0

    def test_loan_denied_when_sum_of_last_five_less_than_amount(self):
        # suma = 49, ostatnie trzy nie wszystkie dodatnie
        self.account.history = [10, -5, 20, -10, 34]
        self.account.balance = 0

        assert self.account.submit_for_loan(50) is False
        assert self.account.balance == 0

    def test_loan_denied_for_non_positive_amount(self):
        self.account.history = [5, 5, 5]  # spełniałoby warunek 3 pozytywnych, ale kwota niepoprawna
        self.account.balance = 10

        assert self.account.submit_for_loan(0) is False
        assert self.account.submit_for_loan(-100) is False
        assert self.account.balance == 10
