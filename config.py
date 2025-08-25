'''
Global configuration settings for the PyBank application.
========================================
This module contains global configuration settings for the PyBank application, including
database connection details, logging settings, and other application-wide parameters.
'''
# The lines `from pathlib import Path` and `from datetime import datetime` are importing specific
# classes from Python modules.
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from tabulate import tabulate
import re

# `BASE_DIR = Path(__file__).resolve().parent` is setting the `BASE_DIR` variable to the parent
# directory of the current script file. Here's a breakdown of what each part of this line does:
BASE_DIR = Path(__file__).resolve().parent

# `DATA_DIR = BASE_DIR / 'data'` is creating a new variable `DATA_DIR` that represents the path to the
# 'data' directory relative to the `BASE_DIR`. The `/` operator in this context is used to concatenate
# paths in Python, resulting in a new path pointing to the 'data' directory within the project's
# directory structure.
DATA_DIR = BASE_DIR / 'data'

# `REPORTS_DIR = BASE_DIR / 'reports'` is creating a new variable `REPORTS_DIR` that represents the
# path to the 'reports' directory relative to the `BASE_DIR`. The `/` operator in this context is used
# to concatenate paths in Python, resulting in a new path pointing to the 'reports' directory within
# the project's directory structure.
REPORTS_DIR = BASE_DIR / 'reports'

# `DOCS_DIR = BASE_DIR / 'docs'` is creating a new variable `DOCS_DIR` that represents the path to the
# 'docs' directory relative to the `BASE_DIR`. The `/` operator in this context is used to concatenate
# paths in Python, resulting in a new path pointing to the 'docs' directory within the project's
# directory structure. This line is essentially defining the location of the 'docs' directory within
# the project.
DOCS_DIR = BASE_DIR / 'docs'

# `DATA_DIR.mkdir(parents=True, exist_ok=True)` is a Python command that creates a directory specified
# by the `DATA_DIR` path variable. Here's a breakdown of what each part of this command does:
DATA_DIR.mkdir(parents=True, exist_ok=True)

# `REPORTS_DIR.mkdir(parents=True, exist_ok=True)` is a Python command that creates the 'reports'
# directory specified by the `REPORTS_DIR` path variable.
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# The line `CUSTOMER_DATA_FILE = DATA_DIR / 'customers.json'` is creating a variable
# `CUSTOMER_DATA_FILE` that represents the path to a specific file named 'customers.json' within the
# 'data' directory of the PyBank project.
CUSTOMER_DATA_FILE = DATA_DIR / 'customers.json'

# The line `TRANSACTION_DATA_FILE = DATA_DIR / 'transactions.json'` is creating a variable
# `TRANSACTION_DATA_FILE` that represents the path to a specific file named 'transactions.json' within
# the 'data' directory of the PyBank project.
TRANSACTION_DATA_FILE = DATA_DIR / 'transactions.json'

# The line `DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'` is defining a format string that specifies how
# dates and times should be represented as strings in the PyBank application.
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# The line `DATE_FORMAT = '%Y-%m-%d'` is defining a format string that specifies how dates should be
# represented as strings in the PyBank application. Specifically, the format `%Y-%m-%d` represents the
# year (4 digits), month (2 digits), and day (2 digits) separated by hyphens.
DATE_FORMAT = '%Y-%m-%d'

# The line `TIME_FORMAT = '%H:%M:%S'` is defining a format string that specifies how time should be
# represented as a string in the PyBank application. Specifically, the format `%H:%M:%S` represents
# the hour (24-hour format), minute, and second separated by colons. This format is used to ensure
# that time values are displayed consistently and in a specific format throughout the application.
TIME_FORMAT = '%H:%M:%S'

# The line `DEFAULT_INITIAL_BALANCE = 0.0` is defining a constant variable named
# `DEFAULT_INITIAL_BALANCE` and assigning it a value of `0.0`. This variable is used to represent the
# default initial balance for accounts in the PyBank application. When a new account is created and no
# specific initial balance is provided, this default value of `0.0` will be used as the starting
# balance.
DEFAULT_INITIAL_BALANCE = 0.0

# The line `CHECKING_INTEREST_RATE = 0.01` is defining a constant variable named
# `CHECKING_INTEREST_RATE` and assigning it a value of `0.01`. This variable represents the interest
# rate for checking accounts in the PyBank application. In this case, the interest rate for checking
# accounts is set to 1% (0.01 as a decimal). This value can be used throughout the application to
# calculate interest on checking account balances or perform other related calculations specific to
# checking accounts.
CHECKING_INTEREST_RATE = 0.01

# The line `SAVING_INTEREST_RATE = 0.03` is defining a constant variable named `SAVING_INTEREST_RATE`
# and assigning it a value of `0.03`. This variable represents the interest rate for savings accounts
# in the PyBank application. In this case, the interest rate for savings accounts is set to 3% (0.03
# as a decimal). This value can be used throughout the application to calculate interest on savings
# account balances or perform other related calculations specific to savings accounts.
SAVING_INTEREST_RATE = 0.03

# The line `LOAN_INTEREST_RATE = 0.07` is defining a constant variable named `LOAN_INTEREST_RATE` and
# assigning it a value of `0.07`. This variable represents the interest rate for loans in the PyBank
# application. In this case, the interest rate for loans is set to 7% (0.07 as a decimal).
LOAN_INTEREST_RATE = 0.07  

# The line `EXCEL_DATE_FORMAT = "YYYY-MM-DD HH:MM:SS"` is defining a constant variable named
# `EXCEL_DATE_FORMAT` and assigning it a specific format string `"YYYY-MM-DD HH:MM:SS"`. This format
# string is likely intended to represent the date and time format in a way that is compatible with
# Excel.
EXCEL_DATE_FORMAT = "YYYY-MM-DD HH:MM:SS"

# The line `EXCEL_DEFAULT_SHEET = "Report"` is defining a constant variable named
# `EXCEL_DEFAULT_SHEET` and assigning it the string value `"Report"`. This variable is likely used to
# specify the default sheet name that should be used when working with Excel files in the PyBank
# application. When creating or interacting with Excel files within the application, this constant can
# be referenced to ensure that the default sheet name is set to "Report" unless explicitly specified
# otherwise.
EXCEL_DEFAULT_SHEET = "Report"

# The line `PROJECT_NAME = "PyBank"` is defining a constant variable named `PROJECT_NAME` and
# assigning it the string value `"PyBank"`. This variable is used to store the name of the project or
# application, in this case, "PyBank". It provides a convenient way to reference the project name
# throughout the codebase, for example, in log messages, reports, or any other place where the project
# name needs to be displayed or used.
PROJECT_NAME = "PyBank"

# The line `DEFAULT_TIME_ZONE = "Africa/Cairo"` is defining a constant variable named
# `DEFAULT_TIME_ZONE` and assigning it the string value `"Africa/Cairo"`. This variable is used to
# store the default time zone setting for the PyBank application. By setting the default time zone to
# "Africa/Cairo", it specifies that the application should use the time zone corresponding to Cairo,
# Egypt as the default time zone for date and time-related operations unless explicitly specified
# otherwise.
DEFAULT_TIME_ZONE = "Africa/Cairo"

# The line `SAVING_WITHDRAWAL_LIMIT = 3` is defining a constant variable named
# `SAVING_WITHDRAWAL_LIMIT` and assigning it the integer value `3`. This variable represents the limit
# on the number of withdrawals allowed for savings accounts in the PyBank application.
SAVING_WITHDRAWAL_LIMIT = 3

# The line `CHECKING_OVERDRAFT_LIMIT = 500.0` is defining a constant variable named
# `CHECKING_OVERDRAFT_LIMIT` and assigning it a value of `500.0`. This variable represents the
# overdraft limit for checking accounts in the PyBank application.
CHECKING_OVERDRAFT_LIMIT = 500.0

# The line `NOW =
# datetime.now(timezone.utc).astimezone(ZoneInfo(DEFAULT_TIME_ZONE)).strftime(DATETIME_FORMAT)` is
# performing the following actions:
NOW = datetime.now(timezone.utc).astimezone(ZoneInfo(DEFAULT_TIME_ZONE)).strftime(DATETIME_FORMAT)


def validation_email(email: str):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email format.")
        return False
    return email

def validation_phone(phone: str):
    if not re.match(r"^(010|011|012|015)\d{8}$", phone):
        print("Invalid email format.")
        return False
    return phone

def render_table(title: str, data: list) -> str:
    table = tabulate(data, tablefmt="grid")
    width = len(table.split("\n")[0]) - 2  
    title_row = "+" + "-" * width + "+"
    title_line = f"| {title.center(width - 2)} |"
    return f"{title_row}\n{title_line}\n{title_row}\n{table}"