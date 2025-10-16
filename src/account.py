import re

class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        if self.is_promo_code_valid(promo_code):
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
