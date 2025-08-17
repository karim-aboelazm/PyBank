from models.account import Account
import config


class CheckingAccount(Account):
    def __init__(self, 
                 account_number: str, 
                 customer_name: str, 
                 customer_id: str, 
                 balance: float = config.DEFAULT_INITIAL_BALANCE,
                 overdraft_limit: float = config.CHECKING_OVERDRAFT_LIMIT):
        super().__init__(account_number, customer_name, customer_id, balance)
        self._overdraft_limit = overdraft_limit
        self._account_type = "Checking Account"

    def withdraw(self, amount: float) -> bool:
        if amount > (self._balance + self._overdraft_limit):
            print(f"Withdrawal of {amount} exceeds overdraft limit of {self._overdraft_limit}.")
            return False
        return super(CheckingAccount,self).withdraw(amount)
    
    def apply_interest(self) -> None:
        if self._balance > 0:
            interest = self._balance * config.CHECKING_INTEREST_RATE
            self._balance += interest
            print(f"Applied interest of {interest} to account {self.get_account_number()}. New balance: {self._balance}")
    
    def get_overdraft_limit(self) -> float:
        """
        The function `get_overdraft_limit` returns the overdraft limit of a checking account.
        
        :return: The method `get_overdraft_limit` is returning the overdraft limit of the checking
        account, which is stored in the `_overdraft_limit` attribute.
        """
        return self._overdraft_limit
    
    def set_overdraft_limit(self, new_limit: float) -> None:
        """
        The function `set_overdraft_limit` sets a new overdraft limit for the checking account.
        
        :param new_limit: The `new_limit` parameter in the `set_overdraft_limit` method represents the
        new overdraft limit that you want to set for the checking account. It is of type `float`, which
        means it can be a decimal number
        """
        if new_limit < 0:
            print("Overdraft limit cannot be negative.")
            return
        self._overdraft_limit = new_limit
        print(f"Overdraft limit set to {self._overdraft_limit} for account {self.get_account_number()}.")
    
    def to_dict(self):
        data = super(CheckingAccount,self).to_dict()
        data['overdraft_limit'] = self._overdraft_limit
        data['account_type'] = self._account_type
        return data
    
    @classmethod
    def from_dict(cls, data):
        account = super(CheckingAccount, cls).from_dict(data)
        account._overdraft_limit = data.get('overdraft_limit', config.CHECKING_OVERDRAFT_LIMIT)
        account._account_type = data.get('account_type', "Checking Account")
        return account