from src.personal_account import PersonalAccount


class TestPersonalAccountLoan:
    def test_loan_granted_when_last_three_are_deposits(self):
        account = PersonalAccount("John", "Doe", "98309201942")
        account.history = [10, -5, 20, 30, 40]  # ostatnie trzy: 20, 30, 40 (wszystkie dodatnie)
        account.balance = 100

        amount = 500
        assert account.submit_for_loan(amount) is True
        assert account.balance == 100 + amount

    def test_loan_granted_when_sum_of_last_five_greater_than_amount(self):
        account = PersonalAccount("Jane", "Doe", "98309201942")
        # Ostatnie trzy nie są wszystkimi wpłatami, ale suma pięciu ostatnich > amount
        account.history = [100, -50, 20, -10, 5]
        account.balance = 0

        amount = 60  # suma ostatnich 5 = 65 > 60
        assert account.submit_for_loan(amount) is True
        assert account.balance == amount

    def test_loan_denied_when_not_enough_history_and_last_three_not_all_deposits(self):
        account = PersonalAccount("John", "Doe", "98309201942")
        account.history = [10, -1]  # mniej niż 3 i mniej niż 5 transakcji
        account.balance = 0

        assert account.submit_for_loan(100) is False
        assert account.balance == 0

    def test_loan_denied_when_sum_of_last_five_equal_to_amount(self):
        account = PersonalAccount("John", "Doe", "98309201942")
        # suma ostatnich pięciu = 50, ostatnie trzy nie są wszystkimi wpłatami
        account.history = [10, -5, 20, -10, 35]
        account.balance = 0

        assert account.submit_for_loan(50) is False  # wymagane: ściśle większa
        assert account.balance == 0

    def test_loan_denied_when_sum_of_last_five_less_than_amount(self):
        account = PersonalAccount("Jane", "Doe", "98309201942")
        # suma = 49, ostatnie trzy nie wszystkie dodatnie
        account.history = [10, -5, 20, -10, 34]
        account.balance = 0

        assert account.submit_for_loan(50) is False
        assert account.balance == 0

    def test_loan_denied_for_non_positive_amount(self):
        account = PersonalAccount("John", "Doe", "98309201942")
        account.history = [5, 5, 5]  # spełniałoby warunek 3 pozytywnych, ale kwota niepoprawna
        account.balance = 10

        assert account.submit_for_loan(0) is False
        assert account.submit_for_loan(-100) is False
        assert account.balance == 10
