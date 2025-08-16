import datetime
import json
from functools import wraps
from config import DATA_DIR,NOW
from services.auth_system import AuthSystem  # so we can get the current user

TRANSACTIONS_FILE = DATA_DIR / "transactions.json"


def log_user_action(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        auth = AuthSystem()  # singleton-like, holds current_user
        user = auth.current_user if auth.is_authenticated() else "anonymous"
        kwargs["user"] = user
        return func(self, *args, **kwargs)
    return wrapper


class TransactionService:
    def __init__(self):
        TRANSACTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not TRANSACTIONS_FILE.exists():
            with open(TRANSACTIONS_FILE, "w") as f:
                json.dump([], f)

    def _save_transaction(self, record):
        with open(TRANSACTIONS_FILE, "r+") as f:
            data = json.load(f)
            data.append(record)
            f.seek(0)
            json.dump(data, f, indent=4)

    @log_user_action
    def deposit(self, account, amount, user=None):
        if amount <= 0:
            print("❌ Deposit amount must be positive.")
            return False

        account.deposit(amount)

        self._save_transaction({
            "type": "deposit",
            "account_id": account.get_account_number(),
            "amount": amount,
            "user": user,
            "timestamp":NOW
        })

        print(f"✅ Deposited {amount:.2f} to account {account.get_account_number()} by {user}.")
        return True

    @log_user_action
    def withdraw(self, account, amount, user=None):
        if account.withdraw(amount):
            self._save_transaction({
                "type": "withdraw",
                "account_id": account.get_account_number(),
                "amount": amount,
                "user": user,
                "timestamp": NOW
            })
            print(f"✅ Withdrawn {amount:.2f} from account {account.get_account_number()} by {user}.")
            return True
        return False

    @log_user_action
    def transfer(self, from_acc, to_acc, amount, user=None):
        if from_acc.withdraw(amount):
            to_acc.deposit(amount)
            self._save_transaction({
                "type": "transfer",
                "from": from_acc.get_account_number(),
                "to": to_acc.get_account_number(),
                "amount": amount,
                "user": user,
                "timestamp": NOW
            })
            print(f"✅ Transferred {amount:.2f} from {from_acc.get_account_number()} to {to_acc.get_account_number()} by {user}.")
            return True
        return False
    
    def get_transactions_for_user(self, username: str) -> list[dict]:
        """Return all transactions made by the specified user."""
        if not TRANSACTIONS_FILE.exists():
            return []

        with open(TRANSACTIONS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []

        # Filter transactions by the user
        return [tx for tx in data if tx.get("user") == username]