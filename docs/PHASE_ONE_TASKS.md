# 🗂 Phase One — Task Breakdown

This document contains **detailed descriptions** for all Phase One tasks of the **PyBank** project.  
Tasks are ordered from **easy → intermediate → advanced**, with **clear deliverables** and **deadlines**.

---

## 📅 Timeline
- **day 1:** Environment setup, configuration, transaction logging.
- **day 2:** Core models for customers & accounts.
- **day 3:** Advanced account types, services, authentication.

---

## 1️⃣ Easy-Level Tasks

### **E1 — Constants & Config File**
**Assigned To:** Ezzat  
**Goal:** Provide a central place for project-wide constants and default configurations.  
**Details:**
- Create a `config.py` file in the root directory.
- Include:
  - **Bank Name** (`PYBANK_NAME`)
  - **Default Currency**
  - **Paths** to `data/` and `reports/`
  - **Withdrawal limits** for checking/savings accounts.
  - **Interest rates** for savings and loans.
  - Default **date format** (`%Y-%m-%d %H:%M:%S`).
- This file will be imported by all services and models.
- Ensure **constants are in ALL_CAPS**.

**Deliverables:**
- `config.py` file committed to GitHub.

**Deadline:** Week 1

---

### **E2 — Transaction Recording System**
**Assigned To:** Mohammed  
**Goal:** Build a logging mechanism for deposits, withdrawals, and transfers.  
**Details:**
- Store transactions in `data/transactions.json` **and** `data/transactions.csv`.
- Each transaction must record:
  - Transaction ID (incremental or UUID)
  - Date/time (`datetime.now()`)
  - Customer ID
  - Account type
  - Transaction type (`deposit`, `withdrawal`, `transfer`)
  - Amount
- Append new transactions without overwriting existing ones.
- Use **`python-dateutil`** for parsing timestamps when loading.

**Deliverables:**
- `services/transactions.py` with `record_transaction()` function.

**Deadline:** Week 1

---

### **E3 — CLI Menu Placeholder**
**Assigned To:** Karim ✅ (Done)  
**Goal:** Create a skeleton CLI menu for future features.  
**Details:**
- Use `rich` for colored menu display.
- Numbered menu items:
  1. Create Customer
  2. Open Account
  3. Deposit
  4. Withdraw
  5. Transfer
  6. Generate Report
  7. Exit
- No functionality yet — just menu navigation structure.

**Deliverables:**
- `main.py` file with `show_menu()` function.

**Deadline:** ✅ Done

---

## 2️⃣ Intermediate-Level Tasks

### **I1 — Customer Class**
**Assigned To:** Mohammed  
**Goal:** Implement an encapsulated customer model.  
**Details:**
- Create `models/customer.py`.
- Attributes:
  - Customer ID (auto-generated)
  - Name
  - Email (validate format)
  - Creation date (`datetime.now()`)
- Methods:
  - `__str__()` for display
  - Getter for ID
  - Setter for name/email with validation
- All attributes should be **private** with getter/setter methods.

**Deliverables:**
- Fully functional `Customer` class with encapsulation.

**Deadline:** Week 2

---

### **I2 — CheckingAccount Class**
**Assigned To:** Ezzat  
**Goal:** Implement a checking account type.  
**Details:**
- Create `models/checking_account.py`.
- Inherit from `Account` base class (Karim will build this in D1).
- Attributes:
  - Monthly fee
  - Overdraft limit
- Methods:
  - Withdraw (respect overdraft limit)
  - Apply monthly fee
- Use `datetime` to track last fee application.

**Deliverables:**
- `CheckingAccount` class with withdraw/fee logic.

**Deadline:** Week 2

---

### **I3 — SavingsAccount Class**
**Assigned To:** Mohammed  
**Goal:** Implement a savings account type.  
**Details:**
- Create `models/savings_account.py`.
- Inherit from `Account` base class (Karim will build this in D1).
- Attributes:
  - Interest rate
  - Withdrawal limit per month
- Methods:
  - Withdraw (enforce limit)
  - Apply interest monthly
- Track last interest application date with `datetime`.

**Deliverables:**
- `SavingsAccount` class with withdrawal/interest logic.

**Deadline:** Week 2

---

## 3️⃣ Advanced-Level Tasks (Senior Developer)

### **D1 — Account Base Class**
**Assigned To:** Karim  
**Goal:** Define a reusable abstract class for all account types.  
**Details:**
- Create `models/account.py`.
- Abstract attributes:
  - Account number (auto-generated)
  - Balance
  - Owner (Customer object)
- Abstract methods:
  - Deposit
  - Withdraw
- Implement:
  - Basic deposit logic
  - `__str__()` for account summary

**Deliverables:**
- `Account` abstract base class with `abc` module.

**Deadline:** Week 2

---

### **D2 — LoanAccount Class**
**Assigned To:** Karim  
**Goal:** Implement debt-based account type.  
**Details:**
- Create `models/loan_account.py`.
- Inherit from `Account`.
- Attributes:
  - Loan amount
  - Interest rate
  - Repayment schedule
- Methods:
  - Disburse loan
  - Repay loan
  - Apply interest monthly
- Track loan start date with `datetime`.

**Deliverables:**
- Fully functional `LoanAccount` class.

**Deadline:** Week 3

---

### **D3 — Bank Service Class**
**Assigned To:** Karim  
**Goal:** Core orchestration layer for the banking system.  
**Details:**
- Create `services/bank_service.py`.
- Manage:
  - Creating customers
  - Opening accounts
  - Deposits/withdrawals/transfers
  - Fetching account/customer data
- All methods must integrate with `transactions.py`.

**Deliverables:**
- `BankService` with CRUD operations.

**Deadline:** Week 3

---

### **D4 — Authentication System**
**Assigned To:** Karim  
**Goal:** Implement secure PIN-based login system.  
**Details:**
- Create `services/auth_system.py`.
- Features:
  - PIN verification
  - Lock account after 3 failed attempts
  - Track last login date/time
- Store user credentials in `data/customers.json`.

**Deliverables:**
- Working authentication system.

**Deadline:** Week 3

---

## 4️⃣ Reporting Task

### **R1 — Excel Reporting Service**
**Assigned To:** Ezzat  
**Goal:** Export filtered transaction history into Excel.  
**Details:**
- Create `services/reporting_service.py`.
- Use:
  - `pandas` for data handling
  - `openpyxl` for Excel export
- Filters:
  - By date range
  - By account type
  - By transaction type
- Save reports in `reports/` folder.

**Deliverables:**
- `generate_report()` function that outputs `.xlsx` file.

**Deadline:** Week 3

---

## ✅ End of Phase One Deliverables
By the end of **Week 3**, we must have:
1. Core banking models (`Customer`, `Account`, `CheckingAccount`, `SavingsAccount`, `LoanAccount`).
2. Transaction recording system.
3. Bank orchestration & authentication services.
4. Excel report generation system.
5. CLI menu skeleton ready for Phase Two integration.

---
