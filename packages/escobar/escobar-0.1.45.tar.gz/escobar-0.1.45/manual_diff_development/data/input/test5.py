class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self._password = self._encrypt_password(password)
        self.is_active = False
        self.login_attempts = 0
        self.last_login = None
    
    def _encrypt_password(self, password):
        # This is a simple simulation of password encryption
        # In a real application, use a proper encryption library
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        encrypted = self._encrypt_password(password)
        return encrypted == self._password
    
    def activate_account(self):
        self.is_active = True
        print(f"Account for {self.username} has been activated.")
    
    def deactivate_account(self):
        self.is_active = False
        print(f"Account for {self.username} has been deactivated.")
    
    def login(self, password):
        if not self.is_active:
            print("Account is not active. Please activate your account first.")
            return False
        
        if self.verify_password(password):
            import datetime
            self.last_login = datetime.datetime.now()
            self.login_attempts = 0
            print(f"Login successful for {self.username}.")
            return True
        else:
            self.login_attempts += 1
            print(f"Invalid password. Login attempts: {self.login_attempts}")
            return False
    
    def reset_password(self, old_password, new_password):
        if self.verify_password(old_password):
            self._password = self._encrypt_password(new_password)
            print("Password has been reset successfully.")
            return True
        else:
            print("Invalid old password. Password reset failed.")
            return False
