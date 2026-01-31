from abc import ABC, abstractmethod
from typing import List
from src.personal_account import PersonalAccount

class AccountsRepository(ABC):
    @abstractmethod
    def save_all(self, accounts: List[PersonalAccount]) -> None:
        pass

    @abstractmethod
    def load_all(self) -> List[PersonalAccount]:
        pass
