import re
import os
import requests
from datetime import date
from src.account import Account


class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        super().__init__(0)
        if len(nip) == 10:
            if not self.validate_nip_mf(nip):
                raise ValueError("Company not registered!!")
            self.nip = nip
        else:
            self.nip = "Invalid"

    def validate_nip_mf(self, nip):
        mf_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")
        today = date.today().strftime("%Y-%m-%d")
        url = f"{mf_url.rstrip('/')}/api/search/nip/{nip}?date={today}"
        try:
            response = requests.get(url)
            res_json = response.json()
            print(res_json)
            if response.status_code == 200 and "result" in res_json and "subject" in res_json["result"] and res_json["result"]["subject"] is not None:
                return res_json["result"]["subject"].get("statusVat") == "Czynny"
        except Exception:
            pass
        return False

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