import re
from src.account import Account


class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        super().__init__(0)
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"

    def is_nip_valid(self, nip):
        if not nip:
            return False
        if len(nip) != 10:
            return False
        return True

    def __register_express_transfer(self, amount):
        express_transfer_fee = 5
        self.history.append(amount)
        self.balance += amount
        self.history.append(-express_transfer_fee)
        self.balance -= express_transfer_fee
        return True

    def try_register_outgoing_express_transfer(self, amount):
        if amount <= 0:
            return False
        if amount > self.balance:
            return False

        return self.__register_express_transfer(-amount)

    def _has_zus_payment(self):
        return -1775 in self.history

    def is_loan_allowed(self, amount):
        if amount <= 0:
            return False

        if self.balance < 2 * amount:
            return False

        if not self._has_zus_payment():
            return False

        return True

    def take_loan(self, amount):
        if not self.is_loan_allowed(amount):
            return False

        self.balance += amount
        return True