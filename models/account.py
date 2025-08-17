import config

class Account:
    '''
        Account model for PyBank application.
        =====================================
        This module defines the Account class, which represents a bank account
        and includes methods for account operations.
    '''
    def __init__(self,account_number:str,customer_name:str,customer_id:str,balance:float=0.0):
        """
            This Python function initializes an object with account number, customer name, balance, and
            creation timestamp.
            
            :param account_number: The `account_number` parameter in the `__init__` method is a string that
            represents the account number of a customer. It is used to uniquely identify the customer's
            account within the system
            :type account_number: str
            :param customer_name: The `customer_name` parameter in the `__init__` method is a string type
            parameter that represents the name of the customer associated with the account
            :type customer_name: str
            :param balance: The `balance` parameter in the `__init__` method of a class represents the
            initial balance of the account associated with the object being created. It is a floating-point
            number that defaults to 0.0 if no initial balance is provided when creating an instance of the
            class
            :type balance: float
        """
        self.__account_number = account_number
        self.__customer_id = customer_id
        self.__customer_name = customer_name
        self._balance = balance
        self._created_at = config.NOW
    
    def get_account_number(self) -> str:
        """
        This function returns the account number of an object.
        :return: The method `get_account_number` is returning the private attribute `__account_number`
        of the class.
        """
        return self.__account_number
    
    def get_customer_name(self) -> str:
        """
        This function returns the customer name stored in the object's `__customer_name` attribute.
        :return: The method `get_customer_name` is returning the value of the `__customer_name`
        attribute of the object.
        """
        return self.__customer_name
    
    def get_customer_id(self) -> str:
        return self.__customer_id
    
    def get_balance(self) -> float:
        """
        The function `get_balance` returns the current balance stored in the object's `_balance`
        attribute.
        :return: The `get_balance` method is returning the current balance stored in the `_balance`
        attribute of the object.
        """
        return self._balance
    
    def get_created_at(self):
        """
        This function returns the value of the `_created_at` attribute of an object.
        :return: The method `get_created_at` is returning the `_created_at` attribute of the object,
        which is expected to be a `datetime` object.
        """
        return self._created_at
    
    def deposit(self, amount: float) -> bool:
        """
        The `deposit` function adds a positive amount to the account balance and returns True, or
        returns False if the amount is not positive.
        
        :param amount: The `amount` parameter in the `deposit` method represents the sum of money that
        is being deposited into the account. It is of type `float`, indicating that it can be a decimal
        number to represent fractional amounts
        :type amount: float
        :return: The `deposit` method is returning a boolean value. It returns `True` if the deposit was
        successful and `False` if the deposit amount is not positive (less than or equal to 0).
        """
        if amount <= 0:
            print("Deposit amount must be positive.")
            return False
        self._balance += amount
        print(f"Deposited {amount} to account {self.__account_number}. New balance: {self._balance}")
        return True
    
    def withdraw(self, amount: float) -> bool:
        """
        The `withdraw` function deducts a specified amount from the account balance if the amount is
        positive and does not exceed the current balance, returning True if successful, or False
        otherwise.
        
        :param amount: The `amount` parameter in the `withdraw` method represents the sum of money that
        is being withdrawn from the account. It is of type `float`, indicating that it can be a decimal
        number to represent fractional amounts
        :type amount: float
        :return: The `withdraw` method is returning a boolean value. It returns `True` if the withdrawal
        was successful (i.e., the amount is positive and does not exceed the current balance), and
        `False` otherwise.
        """
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount > self._balance:
            print("Insufficient funds for withdrawal.")
            return False
        self._balance -= amount
        print(f"Withdrew {amount} from account {self.__account_number}. New balance: {self._balance}")
        return True

    def to_dict(self):
        return {
            "account_number": self.__account_number,
            "customer_id": self.__customer_id,
            "customer_name": self.__customer_name,
            "balance": self._balance,
            "created_at": str(self._created_at),
            "type": self.__class__.__name__ 
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            account_number=data["account_number"],
            customer_id=data["customer_id"],
            customer_name=data["customer_name"],
            balance=data["balance"]
        )

    def __str__(self) -> str:
        """
        This function returns a string representation of an account object, including its account
        number, customer name, balance, and creation date.
        
        :return: The method `__str__` is returning a formatted string that represents the account
        information, including the account number, customer name, balance, and creation date.
        """
        return (
        f"Account\n"
        f"---------------------------\n"
        f" Account No.   : {self.get_account_number()}\n"
        f" Customer ID     : {self.get_customer_id()}\n"
        f" Customer Name     : {self.get_customer_name()}\n"
        f" Balance       : ${self.get_balance():,.2f}\n"
        f" Opened On     : {self.get_created_at()}\n"
    )
