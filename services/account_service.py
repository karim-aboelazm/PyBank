import json
import config
from models import Account, CheckingAccount, SavingsAccount, LoanAccount

# Accounting Data File Store
ACCOUNT_DATA_FILE = config.DATA_DIR / 'accounts.json'


class AccountService:
    def __init__(self):
        # Ensure the data directory exists
        ACCOUNT_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        if not ACCOUNT_DATA_FILE.exists() or ACCOUNT_DATA_FILE.stat().st_size == 0:
            with open(ACCOUNT_DATA_FILE, 'w', encoding="utf-8") as file:
                json.dump([], file)
    
    def _load_all_accounts(self) -> list[Account]:
        try:
            with open(ACCOUNT_DATA_FILE, 'r', encoding="utf-8") as file:
                accounts_data = json.load(file)
            return [Account.from_dict(data) for data in accounts_data]
        except json.JSONDecodeError:
            with open(ACCOUNT_DATA_FILE, 'w', encoding="utf-8") as file:
                json.dump([], file)
            return []
       
    def _save_all_accounts(self, accounts: list[Account]) -> None:
        with open(ACCOUNT_DATA_FILE, 'w', encoding="utf-8") as file:
            json.dump([account.to_dict() for account in accounts], file, indent=4)
    
    def add_account(self, account: Account) -> None:
        accounts = self._load_all_accounts()
        accounts.append(account)
        self._save_all_accounts(accounts)
    
    def get_account(self, account_number: str) -> Account | None:
        accounts = self._load_all_accounts()
        for account in accounts:
            if account.get_account_number() == account_number:
                return account
        return None
    
    def _reconstruct_account(self, account: object) -> Account:
        if isinstance(account, CheckingAccount):
            return CheckingAccount.from_dict(account.to_dict())
        elif isinstance(account, SavingsAccount):
            return SavingsAccount.from_dict(account.to_dict())
        elif isinstance(account, LoanAccount):
            return LoanAccount.from_dict(account.to_dict())
        else:
            return Account.from_dict(account.to_dict())
        
    def get_all_accounts(self) -> list[Account]:
        return [acc for acc in self._load_all_accounts()]
    
    def get_all_customers_accounts(self,customer_id:str) -> list[Account]:
        accounts = self._load_all_accounts()
        return [acc for acc in accounts if acc.get_customer_id() == customer_id]

    def get_customer_accounts(self, customer_id: str = None) -> list[Account]:
        accounts = self._load_all_accounts()
        if customer_id:
            return [acc for acc in accounts if acc.get_customer_id() == customer_id]
        return accounts

    def update_account(self, account: Account) -> bool:
        accounts = self._load_all_accounts()
        update = False
        for i, acc in enumerate(accounts):
            if acc["customer_id"] == account.get_account_number():
                accounts[i] = account
                update = True
                break
        
        if not update:
            print(f"Account not found for update.")

        self._save_all_accounts(accounts)
    
    def delete_account(self, account_number: str) -> bool:
        accounts = self._load_all_accounts()
        accounts = [acc for acc in accounts if acc.get_account_number() != account_number]
        self._save_all_accounts(accounts)
        return True