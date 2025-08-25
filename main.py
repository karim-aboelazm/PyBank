import sys
import os
import getpass
import config
from tabulate import tabulate
from models import SequenceGenerator
from services import BankService, AuthSystem, AccountService, Transaction, CustomerService

# ----------------------------------------------------------------------------- 
# Sequence Generators
# -----------------------------------------------------------------------------
customer_id_gen = SequenceGenerator(prefix="CUST_")
account_id_gen = SequenceGenerator(prefix="ACC_")
user_id_gen = SequenceGenerator(prefix="USER_")

# ----------------------------------------------------------------------------- 
# Clear Screen Function
# -----------------------------------------------------------------------------
def clear_screen():
    input("Press Enter to continue...")
    os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------------------------------------------------------------- 
# Objects and Services Initialization
# -----------------------------------------------------------------------------
bank_service = BankService()
auth_system = AuthSystem()
account_service = AccountService()
transaction_service = Transaction()
customer_service = CustomerService()

# ----------------------------------------------------------------------------- 
# Helper: Menu Renderer
# -----------------------------------------------------------------------------
def render_menu(title: str, options: list[str]) -> str:
    """
    Render a 1-column menu table where the width matches the title width.
    """
    # Prepare data
    data = [[f"{i}. {option}"] for i, option in enumerate(options, start=1)]

    # Render table with tabulate
    table = tabulate(data, tablefmt="grid")

    # Compute widths
    title_width = len(title) + 2  # add padding
    table_width = len(table.splitlines()[0])

    # Ensure table matches title width
    if title_width > table_width - 2:
        diff = title_width - (table_width - 2)
        new_lines = []
        for line in table.splitlines():
            if line.startswith("|"):
                new_lines.append(line[:-1] + " " * diff + "|")
            elif line.startswith("+"):
                new_lines.append(line[:-1] + "-" * diff + "+")
            else:
                new_lines.append(line)
        table = "\n".join(new_lines)
        table_width = len(new_lines[0])

    # Build title
    title_border = "+" + "-" * (table_width - 2) + "+"
    title_row = "|" + title.center(table_width - 2) + "|"

    return f"{title_border}\n{title_row}\n{title_border}\n{table}"

# ----------------------------------------------------------------------------- 
# Authentication Loop Function
# -----------------------------------------------------------------------------
def login_required(func):
    def wrapper(*args, **kwargs):
        if not auth_system.is_authenticated():
            print("Authentication required. Please log in.")
            main()
        return func(*args, **kwargs)
    return wrapper

def main_auth_loop():
    clear_screen()
    menu = render_menu("Authentication Menu", [
        "Register",
        "Login",
        "Exit"
    ])
    print(menu)
    choice = input("Select an option: ")

    if choice == '1':
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone: ")
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        auth_system.register_user(name, username, email, password, phone)
        customer = bank_service.create_customer(
            customer_id_gen.next_id(), name, email, phone, user_id_gen.next_id()
        )
        customer_service.add_customer(customer)
        print(f"Customer {name} with ID {customer.get_customer_id()} added successfully.")
        clear_screen()
    elif choice == '2':
        identifier = input("Enter your email or username: ")
        password = getpass.getpass("Enter your password: ")
        auth_system.login(identifier, password)
        clear_screen()
    elif choice == '3':
        print("Exiting the system. Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid option.")
        clear_screen()

# ----------------------------------------------------------------------------- 
# Customer Menu Function
# -----------------------------------------------------------------------------
@login_required
def get_customer(customer_id: str):
    customer = customer_service.get_customer(customer_id)
    if customer:
        data = [
            ["Customer ID", customer.get_customer_id()],
            ["Related User ID", customer.get_user_id()],
            ["Name", customer.get_customer_name()],
            ["Email", customer.get_customer_email()],
            ["Phone", customer.get_customer_phone()],
        ]
        print(config.render_table("Customer Information", data))
    else:
        print(f"Customer with ID {customer_id} does not exist.")

@login_required
def customer_menu():
    clear_screen()
    menu = render_menu("Customer Menu", [
        "Add Customer",
        "View Customer",
        "View All Related Customers",
        "Update Customers",
        "Delete Customers",
        "Back to Main Menu"
    ])
    print(menu)
    choice = input("Select an option: ")

    if choice == '1':
        customer_name = input("Enter customer name: ")
        customer_email = input("Enter customer email: ")
        customer_phone = input("Enter customer phone: ")
        customer = bank_service.create_customer(
            customer_id_gen.next_id(),
            customer_name,
            customer_email,
            customer_phone,
            auth_system.current_user_id
        )
        customer_service.add_customer(customer)
        print(f"Customer {customer_name} with ID {customer.get_customer_id()} added successfully.")

    elif choice == '2':
        customer_id = input("Enter customer ID to view: ")
        get_customer(customer_id)

    elif choice == '3':
        customers = customer_service.get_customers_by_user(auth_system.current_user_id)
        if customers:
            for i, customer in enumerate(customers, start=1):
                data = [
                    ["Customer ID", customer.get_customer_id()],
                    ["Related User ID", customer.get_user_id()],
                    ["Name", customer.get_customer_name()],
                    ["Email", customer.get_customer_email()],
                    ["Phone", customer.get_customer_phone()],
                ]
                print(config.render_table(f"Customer [{i:02d}] Information", data))
        else:
            print("No customers found.")

    elif choice == '4':
        customer_id = input("Enter customer ID to update: ")
        customer = customer_service.get_customer(customer_id)
        if customer:
            get_customer(customer_id)
            print()
            new_name = input("Enter new name (leave blank to keep current): ") or customer.get_customer_name()
            new_email = input("Enter new email (leave blank to keep current): ") or customer.get_customer_email()
            new_phone = input("Enter new phone (leave blank to keep current): ") or customer.get_customer_phone()
            updated_customer = bank_service.update_customer(customer, new_name, new_email, new_phone)
            customer_service.update_customer(updated_customer)
        else:
            print(f"Customer with ID {customer_id} does not exist.")

    elif choice == '5':
        customer_id = input("Enter customer ID to delete: ")
        if customer_service.get_customer(customer_id):
            customer_service.delete_customer(customer_id)
            print(f"Customer {customer_id} deleted successfully.")
        else:
            print(f"Customer with ID {customer_id} does not exist.")

    elif choice == '6':
        return

# ----------------------------------------------------------------------------- 
# User Menu Function
# -----------------------------------------------------------------------------
@login_required
def get_profile():
    user = auth_system.current_user
    if user:
        data = [
            ["User ID", user['user_id']],
            ["Full Name", user['name']],
            ["Username", user['username']],
            ["Email", user['email']],
            ["Phone", user['phone']],
        ]
        print(config.render_table("Profile Details", data))
    else:
        print("No user is currently logged in.")

@login_required
def user_menu():
    clear_screen()
    menu = render_menu("User Menu", [
        "Profile",
        "Change Password",
        "Reset Password",
        "Back to Main Menu"
    ])
    print(menu)
    choice = input("Select an option: ")

    if choice == '1':
        get_profile()
    elif choice == '2':
        current_password = getpass.getpass("Enter current password: ")
        new_password = getpass.getpass("Enter new password: ")
        auth_system.change_password(current_password, new_password)
    elif choice == '3':
        identifier = input("Enter your email or username for password reset: ")
        new_password = getpass.getpass("Enter new password: ")
        auth_system.reset_password(identifier, new_password)
    elif choice == '4':
        return

# ----------------------------------------------------------------------------- 
# Account Menu Function
# -----------------------------------------------------------------------------
@login_required
def account_menu():
    clear_screen()
    menu = render_menu("Account Menu", [
        "Create Account",
        "View Account",
        "View All Accounts",
        "Back to Main Menu"
    ])
    print(menu)
    choice = input("Select an option: ")

    if choice == '1':
        account_type = input("Enter account type (checking/savings/loan): ").lower()
        customer_id = input("Enter customer ID: ")
        customer = customer_service.get_customer(customer_id)
        if not customer:
            customer_name = input("Enter customer name: ")
        else:
            customer_name = customer.get_customer_name()
        initial_deposit = float(input("Enter initial deposit amount: "))
        account = bank_service.create_account(
            account_type, account_id_gen.next_id(), customer_name, customer_id, initial_deposit
        )
        if account:
            account_service.add_account(account)

    elif choice == '2':
        account_id = input("Enter account ID to view: ")
        account = account_service.get_account(account_id)
        if account:
            print(account.__str__())
        else:
            print(f"Account with number {account_id} does not exist.")

    elif choice == '3':
        customer_id = input("Enter customer ID to filter (leave blank for all): ")
        accounts = account_service.get_all_customers_accounts(customer_id)
        if accounts:
            for i, acc in enumerate(accounts, start=1):
                data = [
                    ["Account No.", acc.get_account_number()],
                    ["Account Type", acc.get_account_type()],
                    ["Customer ID", acc.get_customer_id()],
                    ["Customer Name", acc.get_customer_name()],
                    ["Balance", f"${acc.get_balance():,.2f}"],
                    ["Opened On", acc.get_created_at()],
                ]
                print(config.render_table(f"Account [{i:02d}] Information", data))
        else:
            print("No accounts found.")

    elif choice == '4':
        return

# ----------------------------------------------------------------------------- 
# Transaction Menu Function
# -----------------------------------------------------------------------------
@login_required
def transaction_menu():
    clear_screen()
    menu = render_menu("Transaction Menu", [
        "Deposit",
        "Withdraw",
        "Transfer",
        "View Transactions",
        "Back to Main Menu"
    ])
    print(menu)
    choice = input("Select an option: ")

    if choice == '1':
        account_id = input("Enter account ID for deposit: ")
        amount = float(input("Enter amount to deposit: "))
        account = account_service.get_account(account_id)
        transaction_service.deposit(account, amount, auth_system.current_user['name'])

    elif choice == '2':
        account_id = input("Enter account ID for withdrawal: ")
        amount = float(input("Enter amount to withdraw: "))
        account = account_service.get_account(account_id)
        transaction_service.withdraw(account, amount, auth_system.current_user['name'])

    elif choice == '3':
        from_account_id = input("Enter source account ID: ")
        to_account_id = input("Enter destination account ID: ")
        amount = float(input("Enter amount to transfer: "))
        from_account = account_service.get_account(from_account_id)
        to_account = account_service.get_account(to_account_id)
        transaction_service.transfer(from_account, to_account, amount, auth_system.current_user['name'])

    elif choice == '4':
        account_number = input("Enter account number to view transactions: ")
        transactions = transaction_service.get_transactions(account_number)
        if transactions:
            for txn in transactions:
                print(txn)
        else:
            print(f"No transactions found for account {account_number}.")

    elif choice == '5':
        return

# ----------------------------------------------------------------------------- 
# Main Function
# -----------------------------------------------------------------------------
def main():
    while not auth_system.is_authenticated():
        main_auth_loop()

    while auth_system.is_authenticated():
        clear_screen()
        menu = render_menu(f"Welcome {auth_system.current_user['name']} to PyBank", [
            "Customer Service",
            "User Service",
            "Account Service",
            "Transaction Service",
            "Logout"
        ])
        print(menu)
        choice = input("Select an option: ")

        if choice == '1':
            customer_menu()
        elif choice == '2':
            user_menu()
        elif choice == '3':
            account_menu()
        elif choice == '4':
            transaction_menu()
        elif choice == '5':
            auth_system.logout()
        else:
            print("❌ Invalid option.")

# ----------------------------------------------------------------------------- 
# Entry Point
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    clear_screen()
    print("=== PyBank CLI ===")
    main()
