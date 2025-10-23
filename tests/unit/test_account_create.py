from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "98309201942")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "98309201942"

    def test_pesel_too_long(self):
        account = Account("John", "Doe", "983092034631974")
        assert account.pesel == "Invalid"

    def test_pesel_too_short(self):
        account = Account("John", "Doe", "92019")
        assert account.pesel == "Invalid"

    def test_pesel_empty(self):
        account = Account("John", "Doe", "")
        assert account.pesel == "Invalid"

    def test_no_valid_promo_code(self):
        account = Account("John", "Doe", "98309201942", "PROM_AB1")
        assert account.balance == 0

    def test_no_invalid_promo_code_prefix(self):
        account = Account("John", "Doe", "98309201942", "PROMO_AB1")
        assert account.balance == 50

    def test_no_valid_promo_code_suffix(self):
        account = Account("John", "Doe", "98309201942", "PROM_ABg1")
        assert account.balance == 0

    def test_promo_code_person_born_after_1960_gets_bonus(self):
        account = Account("John", "Doe", "98309201942", "PROMO_ABC")
        assert account.balance == 50

    def test_promo_code_person_born_in_1961_gets_bonus(self):
        account = Account("Jane", "Smith", "61030512345", "PROMO_XYZ")
        assert account.balance == 50

    def test_promo_code_person_born_in_1960_no_bonus(self):
        account = Account("Mark", "Brown", "60123098765", "PROMO_ABC")
        assert account.balance == 0

    def test_promo_code_person_born_before_1960_no_bonus(self):
        account = Account("Alice", "Green", "55081267890", "PROMO_XYZ")
        assert account.balance == 0

    def test_promo_code_person_born_in_1940_no_bonus(self):
        account = Account("Bob", "White", "40030145678", "PROMO_ABC")
        assert account.balance == 0

    def test_promo_code_invalid_pesel_no_bonus(self):
        account = Account("Charlie", "Black", "123", "PROMO_ABC")
        assert account.balance == 0
        assert account.pesel == "Invalid"

    def test_promo_code_person_born_in_2000_gets_bonus(self):
        account = Account("Emily", "Gray", "00222312345", "PROMO_ABC")
        assert account.balance == 50
