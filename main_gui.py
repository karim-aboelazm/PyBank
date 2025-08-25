import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox, QStackedWidget, QFormLayout, QDialog
)
from PyQt5.QtCore import Qt

# Import services and generators
from models import SequenceGenerator
from services import BankService, AuthSystem, AccountService, Transaction, CustomerService


# -------------------------------------------------------------------
# Sequence Generators
# -------------------------------------------------------------------
customer_id_gen = SequenceGenerator(prefix="CUST_")
account_id_gen = SequenceGenerator(prefix="ACC_")
user_id_gen = SequenceGenerator(prefix="USER_")


# -------------------------------------------------------------------
# Initialize Services
# -------------------------------------------------------------------
bank_service = BankService()
auth_system = AuthSystem()
account_service = AccountService()
transaction_service = Transaction()
customer_service = CustomerService()


# -------------------------------------------------------------------
# Login / Register Widget
# -------------------------------------------------------------------
class AuthWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        self.info_label = QLabel("🔑 Login or Register")
        layout.addWidget(self.info_label, alignment=Qt.AlignCenter)

        # Username / Email
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username / Email")
        layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()
        login_btn = QPushButton("Login")
        register_btn = QPushButton("Register")
        button_layout.addWidget(login_btn)
        button_layout.addWidget(register_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Actions
        login_btn.clicked.connect(self.login)
        register_btn.clicked.connect(self.register)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            auth_system.login(username, password)
            self.parent.switch_to_menu()
        except Exception as e:
            QMessageBox.warning(self, "Login Failed", str(e))

    def register(self):
        dialog = RegisterDialog(self)
        dialog.exec_()


# -------------------------------------------------------------------
# Register Dialog
# -------------------------------------------------------------------
class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register New User")
        layout = QFormLayout()

        self.name = QLineEdit()
        self.email = QLineEdit()
        self.phone = QLineEdit()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        layout.addRow("Full Name:", self.name)
        layout.addRow("Email:", self.email)
        layout.addRow("Phone:", self.phone)
        layout.addRow("Username:", self.username)
        layout.addRow("Password:", self.password)

        register_btn = QPushButton("Register")
        layout.addWidget(register_btn)
        self.setLayout(layout)

        register_btn.clicked.connect(self.register_user)

    def register_user(self):
        try:
            auth_system.register_user(
                self.name.text(),
                self.username.text(),
                self.email.text(),
                self.password.text(),
                self.phone.text()
            )
            # Create customer profile
            customer = bank_service.create_customer(
                customer_id_gen.next_id(),
                self.name.text(),
                self.email.text(),
                self.phone.text(),
                user_id_gen.next_id()
            )
            customer_service.add_customer(customer)

            QMessageBox.information(self, "Success", "Registration successful.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# -------------------------------------------------------------------
# Main Menu Widget
# -------------------------------------------------------------------
class MenuWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()

        self.welcome_label = QLabel("👋 Welcome!")
        layout.addWidget(self.welcome_label, alignment=Qt.AlignCenter)

        # Menu Buttons
        customer_btn = QPushButton("Customer Service")
        user_btn = QPushButton("User Service")
        account_btn = QPushButton("Account Service")
        txn_btn = QPushButton("Transaction Service")
        logout_btn = QPushButton("Logout")

        layout.addWidget(customer_btn)
        layout.addWidget(user_btn)
        layout.addWidget(account_btn)
        layout.addWidget(txn_btn)
        layout.addWidget(logout_btn)
        self.setLayout(layout)

        # Actions
        logout_btn.clicked.connect(self.logout)
        customer_btn.clicked.connect(lambda: self.parent.switch_to_page("customer"))
        user_btn.clicked.connect(lambda: self.parent.switch_to_page("user"))
        account_btn.clicked.connect(lambda: self.parent.switch_to_page("account"))
        txn_btn.clicked.connect(lambda: self.parent.switch_to_page("transaction"))

    def logout(self):
        auth_system.logout()
        self.parent.switch_to_auth()


# -------------------------------------------------------------------
# Placeholder Service Pages
# -------------------------------------------------------------------
class CustomerPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📋 Customer Service Page"))
        back_btn = QPushButton("⬅ Back to Menu")
        layout.addWidget(back_btn)
        self.setLayout(layout)
        back_btn.clicked.connect(lambda: self.parent.switch_to_menu())


class UserPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.addWidget(QLabel("👤 User Service Page"))
        back_btn = QPushButton("⬅ Back to Menu")
        layout.addWidget(back_btn)
        self.setLayout(layout)
        back_btn.clicked.connect(lambda: self.parent.switch_to_menu())


class AccountPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.addWidget(QLabel("💰 Account Service Page"))
        back_btn = QPushButton("⬅ Back to Menu")
        layout.addWidget(back_btn)
        self.setLayout(layout)
        back_btn.clicked.connect(lambda: self.parent.switch_to_menu())


class TransactionPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.addWidget(QLabel("💳 Transaction Service Page"))
        back_btn = QPushButton("⬅ Back to Menu")
        layout.addWidget(back_btn)
        self.setLayout(layout)
        back_btn.clicked.connect(lambda: self.parent.switch_to_menu())


# -------------------------------------------------------------------
# Main Window with Stacked Pages
# -------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyBank GUI")
        self.resize(600, 400)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Core widgets
        self.auth_widget = AuthWidget(self)
        self.menu_widget = MenuWidget(self)
        self.customer_page = CustomerPage(self)
        self.user_page = UserPage(self)
        self.account_page = AccountPage(self)
        self.transaction_page = TransactionPage(self)

        # Add all to stack
        self.stack.addWidget(self.auth_widget)      # index 0
        self.stack.addWidget(self.menu_widget)      # index 1
        self.stack.addWidget(self.customer_page)    # index 2
        self.stack.addWidget(self.user_page)        # index 3
        self.stack.addWidget(self.account_page)     # index 4
        self.stack.addWidget(self.transaction_page) # index 5

        self.switch_to_auth()

    def switch_to_auth(self):
        self.stack.setCurrentWidget(self.auth_widget)

    def switch_to_menu(self):
        if auth_system.current_user:
            self.menu_widget.welcome_label.setText(
                f"👋 Welcome, {auth_system.current_user['name']}!"
            )
        self.stack.setCurrentWidget(self.menu_widget)

    def switch_to_page(self, page: str):
        mapping = {
            "customer": self.customer_page,
            "user": self.user_page,
            "account": self.account_page,
            "transaction": self.transaction_page,
        }
        self.stack.setCurrentWidget(mapping[page])


# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
