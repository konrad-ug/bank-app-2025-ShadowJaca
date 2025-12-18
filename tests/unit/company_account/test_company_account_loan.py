import pytest

from src.company_account import CompanyAccount


class TestCompanyAccountLoan:

    @pytest.fixture(autouse=True, scope="function")
    def setup_account(self):
        self.account = CompanyAccount("ACME Sp. z o.o.", "1234567890")

    @pytest.mark.parametrize(
        "history,balance,amount,expected",
        [
            ([-1775], 4000, 1000, True),  # spełnione: saldo >= 2x i jest przelew do ZUS
            ([-1775, 100, -50], 1999, 1000, False),  # saldo < 2x
            ([1000, -100, 1775], 4000, 1000, False),  # brak przelewu -1775 (1775 dodatnie)
            ([-1775], 3000, 0, False),  # niepoprawna kwota
            ([-1775], 3000, -100, False),  # niepoprawna kwota
        ],
    )
    def test_take_loan_business_rules(self, history, balance, amount, expected):
        # arrange
        self.account.history = list(history)
        self.account.balance = balance

        # act
        result = self.account.take_loan(amount)

        # assert
        assert result is expected
        expected_balance = balance + amount if expected else balance
        assert self.account.balance == expected_balance
