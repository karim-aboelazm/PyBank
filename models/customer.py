import config
import re

class Customer:
    def __init__(self, customer_id: str, customer_name: str,customer_email: str,customer_phone, user_id: str):
        self._customer_id = customer_id
        self._customer_name = customer_name
        self._customer_email = customer_email
        self._customer_phone = customer_phone
        self._create_at = config.NOW
        self._user_id = user_id
    
    def get_customer_id(self) -> str:
        return self._customer_id
    
    def get_customer_name(self) -> str:
        return self._customer_name
    
    def get_customer_email(self) -> str:
        return self._customer_email
    
    def get_customer_phone(self) -> str:
        return self._customer_phone
    
    def get_create_at(self):
        return self._create_at
    
    def set_customer_name(self, name: str) -> None:
        if not name:
            print("Customer name cannot be empty.")
            return
        self._customer_name = name
        print(f"Customer name updated to {self._customer_name}.")
    
    def set_customer_email(self, email: str) -> None:
        self._customer_email = config.validation_email(email)
        print(f"Customer email updated to {self._customer_email}.")
    
    def set_customer_phone(self, phone: str) -> None:
        self._customer_phone = config.validation_phone(phone)
        print(f"Customer phone updated to {self._customer_phone}.")
    
    def get_user_id(self) -> str:
        return self._user_id
    
    def set_user_id(self, user_id: str) -> None:
        self._user_id = user_id

    def to_dict(self):
        return {
            'customer_id': self._customer_id,
            'user_id': self._user_id,
            'customer_name': self._customer_name,
            'customer_email': self._customer_email,
            'customer_phone': self._customer_phone,
            'create_at': self._create_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            customer_id=data['customer_id'],
            user_id=data['user_id'],
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            customer_phone=data['customer_phone']
        )