import unittest
from unittest.mock import Mock, patch
from src.mongo_accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount

class TestMongoAccountsRepository(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('src.mongo_accounts_repository.MongoClient')
        self.mock_client_class = self.patcher.start()
        
        # Używamy MagicMock do obsługi metod specjalnych jak __getitem__
        from unittest.mock import MagicMock
        self.mock_client = MagicMock()
        self.mock_client_class.return_value = self.mock_client
        
        self.db_name = 'test_db'
        self.collection_name = 'test_accounts'
        
        # Przygotowanie mocka, aby obsługiwał subskrypcję (client[db_name][collection_name])
        self.mock_collection = MagicMock()
        self.mock_db = MagicMock()
        self.mock_client.__getitem__.return_value = self.mock_db
        self.mock_db.__getitem__.return_value = self.mock_collection

        self.repo = MongoAccountsRepository(db_name=self.db_name, collection_name=self.collection_name)

        self.account1 = PersonalAccount("Jan", "Kowalski", "12345678901")
        self.account1.balance = 100
        self.account1.history = [100]
        
        self.account2 = PersonalAccount("Anna", "Nowak", "12345678902")
        self.account2.balance = 200
        self.account2.history = [200]

    def tearDown(self):
        self.patcher.stop()

    def test_save_all(self):
        accounts = [self.account1, self.account2]
        self.repo.save_all(accounts)
        
        self.mock_collection.delete_many.assert_called_once_with({})
        self.assertEqual(self.mock_collection.update_one.call_count, 2)
        
        # Sprawdzenie czy update_one został wywołany z poprawnymi danymi dla pierwszego konta
        self.mock_collection.update_one.assert_any_call(
            {"pesel": self.account1.pesel},
            {"$set": self.account1.to_dict()},
            upsert=True
        )

    def test_load_all(self):
        self.mock_collection.find.return_value = [
            self.account1.to_dict(),
            self.account2.to_dict()
        ]
        
        loaded_accounts = self.repo.load_all()
        
        self.assertEqual(len(loaded_accounts), 2)
        self.assertEqual(loaded_accounts[0].pesel, self.account1.pesel)
        self.assertEqual(loaded_accounts[0].balance, 100)
        self.assertEqual(loaded_accounts[1].pesel, self.account2.pesel)
        self.assertEqual(loaded_accounts[1].balance, 200)
        self.mock_collection.find.assert_called_once_with({})
