import re
from src.account import Account


class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        super().__init__(0)
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        if self.is_promo_code_valid(promo_code) and self.is_born_after_1960(pesel):
            self.balance += 50

    def is_pesel_valid(self, pesel):

        if not pesel:
            return False

        if len(pesel) != 11:
            return False

        return True

    def is_promo_code_valid(self, code):
        if not code:
            return False

        pattern = r"^PROMO_...$"

        if re.search(pattern, code):
            return True

    def is_born_after_1960(self, pesel):
        """
        Sprawdza czy osoba z danym numerem PESEL urodziła się po 1960 roku.
        Zwraca False jeśli PESEL jest nieprawidłowy.
        """
        if not self.is_pesel_valid(pesel):
            return False

        # Wyciągamy pierwsze dwa znaki reprezentujące rok
        year_digits = int(pesel[:2])
        # Wyciągamy miesiąc (znaki 3-4)
        month = int(pesel[2:4])

        # Określamy stulecie na podstawie miesiąca
        # 1900-1999: miesiąc 01-12
        # 2000-2099: miesiąc 21-32 (dodane 20)
        # 1800-1899: miesiąc 81-92 (dodane 80)
        if month > 80:
            # 1800-1899
            year = 1800 + year_digits
        elif month > 20:
            # 2000-2099
            year = 2000 + year_digits
        else:
            # 1900-1999
            year = 1900 + year_digits

        return year > 1960


    def __register_express_transfer(self, amount):
        express_transfer_fee = 1
        self._register_express__transfer(amount - express_transfer_fee)
        return True

    def try_register_outgoing_express_transfer(self, amount):
        if amount <= 0:
            return False
        if amount > self.balance:
            return False

        return self.__register_express_transfer(-amount)