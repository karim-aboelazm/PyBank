# 📄 PyBank — Phase One Project Plan

## 1️⃣ Project Overview
**PyBank** is a Python-based Banking Management System designed to simulate real-world banking operations while following modern software engineering practices.  
It is developed as a collaborative project with a team of one senior developer and two junior developers.

**Core Goals for Phase One:**
- Establish a clean and scalable **project architecture**.
- Implement **core data models** (Customer, Accounts).
- Set up **bank orchestration services**.
- Integrate **datetime**-based tracking for transactions & reports.
- Prepare **Excel report generation** system.
- Ensure **collaboration-friendly** GitHub workflow.

---

## 2️⃣ Tech Stack
- **Language:** Python 3.10+
- **Data Storage:** JSON / CSV
- **Reporting:** Excel via `openpyxl`
- **CLI Interface:** `rich` & `typer`
- **Testing:** `pytest`
- **Version Control:** Git + GitHub

---

## 3️⃣ Folder Structure

```

PyBank/
│
├── config.py
├── main.py                # CLI entry point
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/                  # Local storage for CSV/JSON
├── reports/               # Generated Excel reports
├── docs/
│   ├── PROJECT\_PLAN.md
│   └── PHASE\_ONE\_TASKS.md
│
├── models/                # All class files
│   ├── **init**.py
│   ├── account.py
│   ├── checking\_account.py
│   ├── savings\_account.py
│   ├── loan\_account.py
│   └── customer.py
│
├── services/              # Core business logic
│   ├── **init**.py
│   ├── bank\_service.py
│   ├── auth\_system.py
│   ├── transactions.py
│   └── reporting\_service.py
│
├── utils/                 # Helper functions
│   └── **init**.py
│
└── tests/                 # Unit tests
├── test\_checking\_account.py
├── test\_savings\_account.py
├── test\_loan\_account.py
└── test\_customer.py

```

---

## 4️⃣ Team Roles
- **Karim (Senior Developer)** → Architecture, advanced OOP, orchestration services, authentication.
- **Mohammed (Junior Developer)** → Customer models, savings account, transaction handling.
- **Ezzat (Junior Developer)** → Config setup, checking account, file/report structure.

---

## 5️⃣ Task Distribution

### **Easy Tasks**
| Task | Assigned To | Description | Deadline |
|------|-------------|-------------|----------|
| E1 — Constants & Config | Ezzat | Create `config.py` with withdrawal limits, interest rates, paths, and default `datetime` settings. | Week 1 |
| E2 — Transaction Recording | Mohammed | Implement consistent transaction logging with timestamps & categories. | Week 1 |
| E3 — CLI Menu Placeholder *(Done)* | Karim | Skeleton CLI with numbered menu options. No functionality. | ✅ Done |

---

### **Intermediate Tasks**
| Task | Assigned To | Description | Deadline |
|------|-------------|-------------|----------|
| I1 — Customer Class | Mohammed | Encapsulated customer model with ID, name, email validation, and creation timestamp. | Week 2 |
| I2 — CheckingAccount | Ezzat | Account type with overdraft prevention, monthly fee, `datetime` tracking. | Week 2 |
| I3 — SavingsAccount | Mohammed | Account type with withdrawal limits, interest, and last interest date tracking. | Week 2 |

---

### **Difficult Tasks**
| Task | Assigned To | Description | Deadline |
|------|-------------|-------------|----------|
| D1 — Account Base Class | Karim | Abstract class for all accounts with core attributes, deposit logic, and abstract methods. | Week 2 |
| D2 — LoanAccount | Karim | Debt-based account type with loan disbursement, repayment, and monthly interest. | Week 3 |
| D3 — Bank Service Class | Karim | Orchestration layer to manage customers, accounts, transfers, and transaction logs. | Week 3 |
| D4 — Authentication System | Karim | Secure PIN-based login, failed attempt lockout, last login tracking. | Week 3 |
| D5 — README & Docs *(Done)* | Karim | Professional `README.md` with setup, features, and branch workflow. | ✅ Done |

---

## 6️⃣ Phase One Timeline

| Week | Focus Area | Expected Deliverables |
|------|------------|-----------------------|
| Week 1 | Config & Transaction Recording | `config.py`, transaction logging system |
| Week 2 | Core Models | `Customer`, `CheckingAccount`, `SavingsAccount`, `Account` base class |
| Week 3 | Advanced Logic & Reports | `LoanAccount`, `BankService`, `auth_system.py` |

---

## 7️⃣ Deliverables by End of Phase One
- Fully functional **core banking models**.
- GitHub repository with **clean folder structure**.
- Excel reporting system **ready for integration**.
- Basic CLI **placeholder menu** in place.
- All tasks tracked in `PHASE_ONE_TASKS.md`.

---

## 8️⃣ GitHub Workflow
- **Main Branch:** Stable, tested code only.
- **Feature Branches:** `feature/<developer>/<feature-name>`
- **Pull Requests:** Required before merging.
- **Code Reviews:** Senior dev reviews junior work before merge.