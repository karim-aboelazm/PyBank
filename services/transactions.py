import datetime
import json
from config import DATA_DIR,NOW
from .auth_system import AuthSystem
from .bank_service import BankService
from models import SequenceGenerator

transation_deposit_id =  SequenceGenerator(prefix="TXN_DEPO_")
transation_withdraw_id = SequenceGenerator(prefix="TXN_WITH_")
transation_transfer_id = SequenceGenerator(prefix="TXN_TRAN_")

TRANSACTIONS_FILE = DATA_DIR / "transactions.json"

class Transaction:
    def __init__(self):
        TRANSACTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not TRANSACTIONS_FILE.exists() or TRANSACTIONS_FILE.stat().st_size == 0:
            with open(TRANSACTIONS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    def _save_transaction(self, transaction_data):
        with open(TRANSACTIONS_FILE, "r+", encoding="utf-8") as f:
            transactions = json.load(f)
            transactions.append(transaction_data)
            f.seek(0)
            json.dump(transactions, f, indent=4)

    def _prepare_transaction_data(self, account, transaction_type, amount,user,account2=None):
        transaction_id = ""
        if transaction_type == "deposit":
            transaction_id = transation_deposit_id.next_id()
        elif transaction_type == "withdraw":
            transaction_id = transation_withdraw_id.next_id()
        elif transaction_type == "transfer":
            transaction_id = transation_transfer_id.next_id()
        else:
            print("Invalid transaction type.")
            return None
        if account2:
            data =  {
                "transaction_id": transaction_id,
                "from_account_number": account.get_account_number(),
                "transaction_type": transaction_type,
                "amount": amount,
                "to_account_number": account2.get_account_number(),
                "user": user,
                "timestamp": NOW,
            }
        else:
            data =  {
                "transaction_id": transaction_id,
                "account_number": account.get_account_number(),
                "transaction_type": transaction_type,
                "amount": amount,
                "user": user,
                "timestamp": NOW,
            }
        return data
    
    def deposit(self, account, amount,user):
        account.deposit(amount)
        transaction_data = self._prepare_transaction_data(account, "deposit", amount,user)
        self._save_transaction(transaction_data)
        return True
    
    def withdraw(self, account, amount,user):
        account.withdraw(amount)
        transaction_data = self._prepare_transaction_data(account, "withdraw", amount,user)
        self._save_transaction(transaction_data)
        return True
    
    def transfer(self, from_account, to_account, amount,user):
        if from_account.withdraw(amount):
            to_account.deposit(amount)
            transaction_data = self._prepare_transaction_data(from_account, "transfer", amount,user,to_account)
            self._save_transaction(transaction_data)
            return True
        return False

    def get_transactions(self, account_number=None):
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            transactions = json.load(f)
        
        if account_number:
            transactions = [t for t in transactions if t.get("account_number") == account_number or t.get("from_account_number") == account_number or t.get("to_account_number") == account_number]
        
        return transactions
    
    def get_transactions_by_date(self, start_date, end_date, account_number=None):
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            transactions = json.load(f)
        
        start_dt = datetime.datetime.fromisoformat(start_date)
        end_dt = datetime.datetime.fromisoformat(end_date)
        
        filtered_transactions = []
        for t in transactions:
            t_dt = datetime.datetime.fromisoformat(t["timestamp"])
            if start_dt <= t_dt <= end_dt:
                if account_number:
                    if t.get("account_number") == account_number or t.get("from_account_number") == account_number or t.get("to_account_number") == account_number:
                        filtered_transactions.append(t)
                else:
                    filtered_transactions.append(t)
        
        return filtered_transactions
    
    def get_transactions_by_type(self, transaction_type, account_number=None):
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            transactions = json.load(f)
        
        filtered_transactions = [t for t in transactions if t["transaction_type"] == transaction_type]
        
        if account_number:
            filtered_transactions = [t for t in filtered_transactions if t.get("account_number") == account_number or t.get("from_account_number") == account_number or t.get("to_account_number") == account_number]
        
        return filtered_transactions
    
    def get_transactions_by_user(self, user_email, account_number=None):
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            transactions = json.load(f)
        
        filtered_transactions = [t for t in transactions if t["user"] == user_email]
        
        if account_number:
            filtered_transactions = [t for t in filtered_transactions if t.get("account_number") == account_number or t.get("from_account_number") == account_number or t.get("to_account_number") == account_number]
        
        return filtered_transactions
    
    def get_transactions_by_customer_id(self, customer_id, account_number=None):
        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            transactions = json.load(f)

        bank_service = BankService()
        accounts = bank_service.get_customer_accounts(customer_id)
        account_numbers = {acc.get_account_number() for acc in accounts}
        filtered_transactions = [t for t in transactions if t.get("account_number") in account_numbers or t.get("from_account_number") in account_numbers or t.get("to_account_number") in account_numbers]
        if account_number:
            filtered_transactions = [t for t in filtered_transactions if t.get("account_number") == account_number or t.get("from_account_number") == account_number or t.get("to_account_number") == account_number]
        return filtered_transactions
    