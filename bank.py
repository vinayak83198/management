# bank.py
import json
import random
import string
from pathlib import Path


class Bank:
    database = 'data.json'
    data = []

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            try:
                with open(cls.database) as fs:
                    cls.data = json.load(fs)
            except Exception as err:
                print(f"An exception occurred: {err}")
        else:
            print("No such file exists")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def __accountgenerate(cls):
        acc_id_parts = (
            random.choices(string.ascii_letters, k=3) +
            random.choices(string.digits, k=3) +
            random.choices("!@#$^&*", k=1)
        )
        random.shuffle(acc_id_parts)
        return "".join(acc_id_parts)

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return None, "Account creation failed: Must be 18+ and use a 4-digit PIN."

        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo.": cls.__accountgenerate(),
            "balance": 0
        }

        cls.data.append(info)
        cls.__update()
        return info, "Account created successfully."

    @classmethod
    def authenticate(cls, accnumber, pin):
        return [user for user in cls.data if user['accountNo.'] == accnumber and user['pin'] == pin]

    @classmethod
    def deposit(cls, accnumber, pin, amount):
        user = cls.authenticate(accnumber, pin)
        if not user:
            return False, "Account not found."
        if not (0 < amount <= 10000):
            return False, "Amount must be between 1 and 10000."
        user[0]['balance'] += amount
        cls.__update()
        return True, "Amount deposited successfully."

    @classmethod
    def withdraw(cls, accnumber, pin, amount):
        user = cls.authenticate(accnumber, pin)
        if not user:
            return False, "Account not found."
        if user[0]['balance'] < amount:
            return False, "Insufficient balance."
        user[0]['balance'] -= amount
        cls.__update()
        return True, "Amount withdrawn successfully."

    @classmethod
    def get_details(cls, accnumber, pin):
        user = cls.authenticate(accnumber, pin)
        return user[0] if user else None

    @classmethod
    def update_details(cls, accnumber, pin, name=None, email=None, new_pin=None):
        user = cls.authenticate(accnumber, pin)
        if not user:
            return False, "Account not found."

        if name:
            user[0]['name'] = name
        if email:
            user[0]['email'] = email
        if new_pin:
            user[0]['pin'] = int(new_pin)

        cls.__update()
        return True, "Details updated successfully."

    @classmethod
    def delete_account(cls, accnumber, pin):
        user = cls.authenticate(accnumber, pin)
        if not user:
            return False, "Account not found."
        cls.data.remove(user[0])
        cls.__update()
        return True, "Account deleted successfully."
