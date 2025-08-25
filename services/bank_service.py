import config
from models import Account, CheckingAccount, SavingsAccount, LoanAccount, Customer

class BankService:
    def __init__(self):
        self._accounts = {}  # {account_number: Account()}
        self._customers = {} # {customer_id: Customer()}
    
    # Customer Management
    def create_customer(self, customer_id, name, email, phone,user_id) -> Customer:
        if customer_id in self._customers:
            print(f"Customer with ID {customer_id} already exists.")
            return None
        if not config.validation_email(email):
            print("Invalid email format.")
            return None
        if not config.validation_phone(phone):
            print("Invalid phone number format.")
            return None
        customer = Customer(customer_id, name, email, phone,user_id)
        self._customers[customer_id] = customer
        return customer
    
    def get_customer(self, customer_id) -> Customer:
        return self._customers.get(customer_id)
    
    def update_customer(self, customer: Customer, name=None, email=None, phone=None):
        if not customer:
            print("Customer does not exist.")
            return None
        if name and name.strip():
            customer.set_customer_name(name)
        if email and email.strip():
            customer.set_customer_email(email)
        if phone and phone.strip():
            customer.set_customer_phone(phone)
        print("Customer updated successfully.")
        return customer

    # Account Management
    def create_account(self, account_type: str, account_number: str, customer_id: str, customer_name: str, initial_deposit: float = 0.0) -> Account:
        if account_type == "checking":
            account = CheckingAccount(account_number, customer_id, customer_name, initial_deposit)
        elif account_type == "savings":
            account = SavingsAccount(account_number, customer_id, customer_name, initial_deposit)
        elif account_type == "loan":
            account = LoanAccount(account_number, customer_id, customer_name, initial_deposit)
        else:
            print(f"Invalid account type: {account_type}")
            return None
        
        self._accounts[account_number] = account
        print(f"{account_type.capitalize()} account {account_number} created successfully for customer {customer_name}.")
        return account

    def get_account(self, account_number: str) -> Account:
        return self._accounts.get(account_number)
    
    def get_customer_accounts(self, customer_id: str) -> list:
        return [acc for acc in self._accounts.values() if acc.get_customer_id() == customer_id]
    
    # Transaction Management
    def deposit(self, account_number: str, amount: float) -> bool:
        account = self.get_account(account_number)
        if not account:
            print(f"Account {account_number} not found.")
            return False
        if amount <= 0:
            print("Deposit amount must be positive.")
            return False
        account.deposit(amount)
        print(f"Deposited {amount} to account {account_number}. New balance: {account.get_balance()}")
        return True
    
    def withdraw(self, account_number: str, amount: float) -> bool:
        account = self.get_account(account_number)
        if not account:
            print(f"Account {account_number} not found.")
            return False
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if account.withdraw(amount):
            print(f"Withdrew {amount} from account {account_number}. New balance: {account.get_balance()}")
            return True
        else:
            print(f"Insufficient funds for withdrawal from account {account_number}. Current balance: {account.get_balance()}")
            return False
    
    def transfer(self, from_account_number: str, to_account_number: str, amount: float) -> bool:
        from_account = self.get_account(from_account_number)
        to_account = self.get_account(to_account_number)
        
        if not from_account:
            print(f"Source account {from_account_number} not found.")
            return False
        if not to_account:
            print(f"Destination account {to_account_number} not found.")
            return False
        if amount <= 0:
            print("Transfer amount must be positive.")
            return False
        
        if from_account.withdraw(amount):
            to_account.deposit(amount)
            print(f"Transferred {amount} from account {from_account_number} to account {to_account_number}.")
            return True
        else:
            print(f"Insufficient funds for transfer from account {from_account_number}. Current balance: {from_account.get_balance()}")
            return False
    
    # Reporting Management
    def get_account_summary(self, account_number: str) -> str:
        account = self.get_account(account_number)
        if not account:
            print(f"Account {account_number} not found.")
            return {}
        return account.__str__()

    def get_customer_accounts(self, customer_id: str) -> list:
        if customer_id not in self._customers:
            print(f"Customer with ID {customer_id} does not exist.")
            return []
        accounts = [acc.__str__() for acc in self._accounts.values() if acc.get_customer_id() == customer_id]
        return accounts