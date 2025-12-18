from typing import Optional, Dict, List

from src.personal_account import PersonalAccount


class AccountsRegistry:
    """
    Prosty rejestr kont osobistych działający w pamięci (POC).
    Zapewnia unikalność PESEL i identyfikatory auto‑inkrementujące.
    """

    def __init__(self) -> None:
        self._next_id: int = 1
        self._by_id: Dict[int, PersonalAccount] = {}
        self._id_by_pesel: Dict[str, int] = {}

    def _is_pesel_valid(self, pesel: Optional[str]) -> bool:
        if not pesel:
            return False
        return len(pesel) == 11

    def add_personal_account(
        self,
        first_name: str,
        last_name: str,
        pesel: str,
        promo_code: Optional[str] = None,
    ) -> int:
        """
        Dodaje konto osobiste, zwraca jego nowy identyfikator.
        Rzuca ValueError, gdy PESEL jest niepoprawny lub już istnieje w rejestrze.
        """
        if not self._is_pesel_valid(pesel):
            raise ValueError("PESEL invalid")
        if pesel in self._id_by_pesel:
            raise ValueError("Account with this PESEL already exists")

        account = PersonalAccount(first_name, last_name, pesel, promo_code)

        new_id = self._next_id
        self._next_id += 1

        self._by_id[new_id] = account
        self._id_by_pesel[pesel] = new_id
        return new_id

    def get_by_id(self, account_id: int) -> Optional[PersonalAccount]:
        return self._by_id.get(account_id)

    def get_by_pesel(self, pesel: str) -> Optional[PersonalAccount]:
        acc_id = self._id_by_pesel.get(pesel)
        return self._by_id.get(acc_id) if acc_id is not None else None

    def list_all(self) -> List[PersonalAccount]:
        return list(self._by_id.values())

    def remove(self, account_id: int) -> bool:
        account = self._by_id.pop(account_id, None)
        if account is None:
            return False

        pesel = account.pesel
        if pesel in self._id_by_pesel and self._id_by_pesel[pesel] == account_id:
            del self._id_by_pesel[pesel]

        return True
