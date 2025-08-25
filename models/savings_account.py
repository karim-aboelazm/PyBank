from models.account import Account
import config

class SavingsAccount(Account):
    def __init__(self, 
                 account_number: str, 
                 customer_name: str, 
                 customer_id: str, 
                 balance: float = config.DEFAULT_INITIAL_BALANCE,
                 interest_rate: float = config.SAVING_INTEREST_RATE,
                 account_type: str = "Savings Account"):
        super().__init__(account_number, customer_name, customer_id, balance)
        self._interest_rate = interest_rate
        self._withdrawals_this_month = 0
        self._withdrawal_limit = config.SAVING_WITHDRAWAL_LIMIT
        self._account_type = account_type
    
    def withdraw(self, amount):
        if self._withdrawals_this_month >= self._withdrawal_limit:
            print(f"Withdrawal limit of {self._withdrawal_limit} reached for this month.")
            return False
        return super(SavingsAccount,self).withdraw(amount)
    
    def apply_interest(self):
        if self._balance > 0:
            interest = self._balance * self._interest_rate
            self._balance += interest
            print(f"Applied interest of {interest} to account {self.get_account_number()}. New balance: {self._balance}")
    
    def get_interest_rate(self) -> float:
        return self._interest_rate
    
    def set_interest_rate(self, rate: float) -> None:
        if rate < 0:
            print("Interest rate cannot be negative.")
            return
        self._interest_rate = rate
        print(f"Interest rate set to {self._interest_rate} for account {self.get_account_number()}.")
    
    def get_withdrawal_limit(self) -> int:
        return self._withdrawal_limit
    
    def set_withdrawal_limit(self, limit: int) -> None:
        if limit < 0:
            print("Withdrawal limit cannot be negative.")
            return
        self._withdrawal_limit = limit
        print(f"Withdrawal limit set to {self._withdrawal_limit} for account {self.get_account_number()}.")
    
    def get_withdrawals_this_month(self) -> int:
        return self._withdrawals_this_month
    
    def set_withdrawals_this_month(self, count: int) -> None:
        if count < 0:
            print("Withdrawal count cannot be negative.")
            return
        self._withdrawals_this_month = count
        print(f"Withdrawals this month set to {self._withdrawals_this_month} for account {self.get_account_number()}.")
    
    def reset_withdrawals_this_month(self) -> None:
        self._withdrawals_this_month = 0
        print(f"Withdrawals this month reset for account {self.get_account_number()}.")
    
    def get_account_type(self) -> str:
        return self._account_type

    def to_dict(self):
        data = super(SavingsAccount, self).to_dict()
        data['interest_rate'] = self._interest_rate
        data['withdrawals_this_month'] = self._withdrawals_this_month
        data['withdrawal_limit'] = self._withdrawal_limit
        data['account_type'] = self._account_type
        return data
    
    @classmethod
    def from_dict(cls, data):
        account = super(SavingsAccount, cls).from_dict(data)
        account._interest_rate = data.get('interest_rate', config.SAVING_INTEREST_RATE)
        account._withdrawals_this_month = data.get('withdrawals_this_month', 0)
        account._withdrawal_limit = data.get('withdrawal_limit', config.SAVING_WITHDRAWAL_LIMIT)
        account._account_type = data.get('account_type', "Savings Account")
        return account

    