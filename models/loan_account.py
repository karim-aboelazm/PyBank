from models.account import Account
import config


class LoanAccount(Account):
    def __init__(self, 
                 account_number: str, 
                 customer_name: str, 
                 customer_id: str, 
                 balance: float = config.DEFAULT_INITIAL_BALANCE, 
                 loan_amount: float = 0.0,
                 interest_rate: float = config.LOAN_INTEREST_RATE,
                 term_months: int = 12,
                 account_type: str = "Loan Account"):
        super().__init__(account_number, customer_name, customer_id, balance)
        self._loan_amount = loan_amount
        self._interest_rate = interest_rate
        self._term_months = term_months
        self._monthly_installments = self.calculate_monthly_installment()
        self._account_type = account_type

    def calculate_monthly_installment(self) -> float:
        if self._term_months <= 0:
            return 0.0
        total_interests = self._loan_amount * self._interest_rate * (self._term_months / 12)
        total_payable = self._loan_amount + total_interests
        installment = total_payable / self._term_months
        return round(installment, 2)

    def repay_loan(self, amount: float) -> bool:
        if amount < self._monthly_installments:
            print(f"Repayment amount {amount} is less than the monthly installment {self._monthly_installments}.")
            return False
        self._loan_amount -= amount
        if self._loan_amount < 0:
            self._loan_amount = 0
            print("Loan fully repaid.")
        print(f"Repaid {amount}. Remaining loan amount: {self._loan_amount}.")
        return True

    def get_loan_amount(self) -> float:
        return self._loan_amount
    
    def set_loan_amount(self, amount: float) -> None:
        if amount < 0:
            print("Loan amount cannot be negative.")
            return
        self._loan_amount = amount
        self._monthly_installments = self.calculate_monthly_installment()
        print(f"Loan amount set to {self._loan_amount}. Monthly installment: {self._monthly_installments}.")
    
    def get_interest_rate(self) -> float:
        return self._interest_rate
    
    def set_interest_rate(self, rate: float) -> None:
        if rate < 0:
            print("Interest rate cannot be negative.")
            return
        self._interest_rate = rate
        self._monthly_installments = self.calculate_monthly_installment()
        print(f"Interest rate set to {self._interest_rate}. Monthly installment: {self._monthly_installments}.")

    def get_term_months(self) -> int:
        return self._term_months
    
    def set_term_months(self, months: int) -> None:
        if months <= 0:
            print("Term months must be positive.")
            return
        self._term_months = months
        self._monthly_installments = self.calculate_monthly_installment()
        print(f"Term set to {self._term_months} months. Monthly installment: {self._monthly_installments}.")

    def get_monthly_installment(self) -> float:
        return self._monthly_installments
    
    def get_account_type(self) -> str:
        return self._account_type

    def to_dict(self):
        data = super(LoanAccount, self).to_dict()
        data['loan_amount'] = self._loan_amount
        data['interest_rate'] = self._interest_rate
        data['term_months'] = self._term_months
        data['monthly_installment'] = self._monthly_installments
        data['account_type'] = self._account_type
        return data
    
    @classmethod
    def from_dict(cls, data):
        account = super(LoanAccount, cls).from_dict(data)
        account._loan_amount = data.get('loan_amount', 0.0)
        account._interest_rate = data.get('interest_rate', config.LOAN_INTEREST_RATE)
        account._term_months = data.get('term_months', 12)
        account._monthly_installments = account.calculate_monthly_installment()
        account._account_type = data.get('account_type', "Loan Account")
        return account

