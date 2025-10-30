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
        self._register_express__transfer(amount - express_transfer_fee)
        return True

    def try_register_outgoing_express_transfer(self, amount):
        if amount <= 0:
            return False
        if amount > self.balance:
            return False

        return self.__register_express_transfer(-amount)