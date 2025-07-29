class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self._password = self._encrypt_password(password)
        self.is_active = False
        self.login_attempts = 0
        self.last_login = None

    def _encrypt_password(self, password):
        # Using a library for password hashing
        import bcrypt
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password):
        import bcrypt
        return bcrypt.checkpw(password.encode(), self._password)

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

        # Simplified login logic with security checks
        if self.verify_password(password):
            self._update_login_status(True)
            return True
        else:
            self._update_login_status(False)
            return False

    def _update_login_status(self, success):
        import datetime
        if success:
            self.last_login = datetime.datetime.now()
            self.login_attempts = 0
            print(f"Login successful for {self.username}.")
        else:
            self.login_attempts += 1
            print(f"Invalid password. Login attempts: {self.login_attempts}")
            if self.login_attempts >= 3:
                print("Account locked due to too many failed attempts.")
                self.is_active = False

    def reset_password(self, old_password, new_password):
        if self.verify_password(old_password):
            self._password = self._encrypt_password(new_password)
            print("Password has been reset successfully.")
            return True
        else:
            print("Invalid old password. Password reset failed.")
            return False
