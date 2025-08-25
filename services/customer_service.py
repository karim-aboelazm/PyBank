import os
import json
import config
from pathlib import Path
from models import Customer

CUSTOMERS_FILE = config.DATA_DIR /"customers.json"

class CustomerService:
    def __init__(self):
        CUSTOMERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        if not CUSTOMERS_FILE.exists() or CUSTOMERS_FILE.stat().st_size == 0:
            with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    def load_customers(self):
        with open(CUSTOMERS_FILE, "r", encoding="utf-8") as f:
            customers_data = json.load(f)
        customers = [Customer.from_dict(data) for data in customers_data]
        return customers

    def save_customers(self, customers):
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump([customer.to_dict() for customer in customers], f, indent=4)

    def add_customer(self, customer: Customer):
        customers = self.load_customers()
        if any(c.get_customer_id() == customer.get_customer_id() for c in customers):
            print(f"Customer with ID {customer.get_customer_id()} already exists.")
            return False
        customers.append(customer)
        self.save_customers(customers)
        return True
    
    def get_customer(self, customer_id: str):
        customers = self.load_customers()
        for customer in customers:
            if customer.get_customer_id() == customer_id:
                return customer
        print(f"❌❌ Customer with ID {customer_id} not found.")
        return None

    def get_customers_by_user(self, user_id: str):
        customers = self.load_customers()
        user_customers = [c for c in customers if c.get_user_id() == user_id]
        return user_customers

    def update_customer(self, updated_customer: Customer):
        customers = self.load_customers()
        for i, customer in enumerate(customers):
            if customer.customer_id == updated_customer.customer_id:
                customers[i] = updated_customer
                self.save_customers(customers)
                print(f"Customer {updated_customer.name} updated successfully.")
                return True
        print(f"Customer with ID {updated_customer.customer_id} not found.")
        return False
    
    def delete_customer(self, customer_id: str):
        customers = self.load_customers()
        customers = [c for c in customers if c.customer_id != customer_id]
        self.save_customers(customers)
        print(f"Customer with ID {customer_id} deleted successfully.")
        return True
    