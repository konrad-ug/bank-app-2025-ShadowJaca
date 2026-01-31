from pymongo import MongoClient
from typing import List
from src.personal_account import PersonalAccount
from src.accounts_repository import AccountsRepository

class MongoAccountsRepository(AccountsRepository):
    def __init__(self, host='localhost', port=27017, db_name='bank', collection_name='accounts'):
        self._client = MongoClient(host, port)
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

    def save_all(self, accounts: List[PersonalAccount]) -> None:
        self._collection.delete_many({})
        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()},
                upsert=True,
            )

    def load_all(self) -> List[PersonalAccount]:
        accounts_data = self._collection.find({})
        return [PersonalAccount.from_dict(data) for data in accounts_data]
