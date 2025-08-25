import json
import hashlib
import config
from models import SequenceGenerator

user_id_gen = SequenceGenerator(prefix="USER_")


# Users Data File Store
USER_DATA_FILE = config.DATA_DIR / 'users.json'

class AuthSystem:
    def __init__(self):
        self.current_user = None
        self.current_user_id = None
        # Ensure the data directory exists
        USER_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        if not USER_DATA_FILE.exists() or USER_DATA_FILE.stat().st_size == 0:
            with open(USER_DATA_FILE, 'w', encoding="utf-8") as file:
                json.dump([], file)
    
    def _load_all_users(self) -> list[dict]:
        try:
            with open(USER_DATA_FILE, 'r', encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            with open(USER_DATA_FILE, 'w', encoding="utf-8") as file:
                json.dump([], file)
            return []
    
    def _save_all_users(self, users: list[dict]) -> None:
        with open(USER_DATA_FILE, 'w', encoding="utf-8") as file:
            json.dump(users, file, indent=4)
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def register_user(self,name:str, username: str, email:str, password: str,phone:str) -> bool:
        all_users = self._load_all_users()
        if any(user['email'] == email for user in all_users):
            print("User with `Email` already registered.")
            return False
        
        if any(user['username'] == username for user in all_users):
            print("User with `Username` already registered.")
            return False
        if not config.validation_email(email):
            print("Invalid email format.")
            return False
        if not config.validation_phone(phone):
            print("Invalid phone number format.")
            return False
        user_id = user_id_gen.next_id()
        all_users.append({
            'user_id':user_id,
            'name': name,
            'username': username,
            'email': email,
            'phone': phone,
            'password': self._hash_password(password)
        })
        self._save_all_users(all_users)
        print("User registered successfully.")
        return True

    def login(self, identifier: str, password: str) -> bool:
        all_users = self._load_all_users()
        hashed_password = self._hash_password(password)
        for user in all_users:
            if '@' in identifier:
                config.validation_email(identifier)
                if user['email'] == identifier and user['password'] == hashed_password:
                    self.current_user = user
                    self.current_user_id = user['user_id']
                    print(f"Welcome {user['name']}!")
                    return True
            else:
                if user['username'] == identifier and user['password'] == hashed_password:
                    self.current_user = user
                    self.current_user_id = user['user_id']
                    print(f"Welcome {user['name']}!")
                    return True
        print("Invalid email or password.")
        return False
    
    def reset_password(self, identifier: str, new_password: str) -> bool:
        all_users = self._load_all_users()
        for user in all_users:
            if '@' in identifier:
                config.validation_email(identifier)
                if user['email'] == identifier:
                    user['password'] = self._hash_password(new_password)
                    self._save_all_users(all_users)
                    print("Password reset successfully.")
                    return True
            else:
                if user['username'] == identifier:
                    user['password'] = self._hash_password(new_password)
                    self._save_all_users(all_users)
                    print("Password reset successfully.")
                    return True
        print("User not found.")
        return False

    def forget_password(self, identifier: str) -> bool:
        all_users = self._load_all_users()
        for user in all_users:
            if '@' in identifier:
                config.validation_email(identifier)
                if user['email'] == identifier:
                    print("Password reset link sent to your email. please make reset password.")
                    print(f"please enter your email [{user['email']}] and your new password.")
                    return True
            else:
                if user['username'] == identifier:
                    print("Password reset link sent to your username. please make reset password.")
                    print(f"please enter your username [{user['username']}] and your new password.")
                    return True
        print("User not found.")
        return False

    def change_password(self, old_password: str, new_password: str) -> bool:
        if not self.is_authenticated():
            print("No user is currently logged in.")
            return False
        
        if self._hash_password(old_password) != self.current_user['password']:
            print("Old password is incorrect.")
            return False
        
        self.current_user['password'] = self._hash_password(new_password)
        all_users = self._load_all_users()
        
        for i, user in enumerate(all_users):
            if user['username'] == self.current_user['username']:
                all_users[i] = self.current_user
                break
        
        self._save_all_users(all_users)
        print("Password changed successfully.")
        return True

    def logout(self) -> None:
        if self.current_user:
            print(f"Goodbye {self.current_user['name']}!")
            self.current_user = None
            self.current_user_id = None
        else:
            print("No user is currently logged in.")

    def get_current_user(self) -> dict | None:
        return self.current_user
    
    def is_authenticated(self) -> bool:
        return self.current_user is not None