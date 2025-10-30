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