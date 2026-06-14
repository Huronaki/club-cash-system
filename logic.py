import csv
from datetime import datetime

class User:


    def __init__(self, username, password, role):

        self.username = username
        self.password = password
        self.role = role


class Admin(User):


    def __init__(self, username, password):
        super().__init__(username, password, 'admin')
    
    
    def create_account(self, account_name):
        return Account(account_name)
    
    
    def create_user(self, username, password, role):
        if role == "treasurer":
            return Treasurer(username, password)
        elif role == "finance_officer":
            return FinanceOfficer(username, password)
        raise ValueError("Invalid role")


class Treasurer(User):

    
    def __init__(self, username, password):
        super().__init__(username, password, 'treasurer')


class FinanceOfficer(User):
    
    def __init__(self, username, password):
        super().__init__(username, password, 'finance_officer')


class Account:
    
    def __init__(self, name):

        self.name = name
        self.balance = 0.0
        self.transactions = []
    
    
    def add_transaction(self, transaction_type, amount, transactions_source, transaction_target):

        transaction = {
            'date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'type': transaction_type,
            'amount': amount,
            'source': transactions_source,
            'target': transaction_target,
            'balance': self.balance
        }
        self.transactions.append(transaction)
    
    
    def deposit(self, amount, source):

        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        self.add_transaction('deposit', amount, source, self.name)
        
        
    def withdraw(self, amount, target):

        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.add_transaction('withdraw', amount, self.name, target)
    
    
    def transfer(self, amount, target_account):

        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        target_account.balance += amount
        
        self.add_transaction("transfer", amount, self.name, target_account.name)
        target_account.add_transaction("transfer", amount, self.name, target_account.name)
    
    
    def get_transaction_history(self):

        return self.transactions


class SystemManager:

    
    @staticmethod
    def save_accounts(accounts, file_name):

        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Balance"])
            for account in accounts:
                writer.writerow([account.name, account.balance])


    @staticmethod
    def load_accounts(file_name):

        accounts = []
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Name']
                balance = float(row['Balance'])
                
                account = Account(name)
                account.balance = balance
                accounts.append(account)
        return accounts


    @staticmethod
    def save_transactions(account, file_name):

        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Amount", "Source", "Target", "Balance"])
            for transaction in account.get_transaction_history():
                writer.writerow(transaction.values())


    @staticmethod
    def load_transactions(file_name):

        transactions = []
        with open(file_name, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)
        return transactions


    @staticmethod
    def save_users(users, file_name):

        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password", "Role"])
            for user in users.values():
                writer.writerow([user.username, user.password, user.role])


    @staticmethod
    def load_users(file_name):

        users = {}
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row["Username"]
                password = row["Password"]
                role = row["Role"]
                if role == "admin":
                    users[username] = Admin(username, password)
                elif role == "treasurer":
                    users[username] = Treasurer(username, password)
                elif role == "finance_officer":
                    users[username] = FinanceOfficer(username, password)
                else:
                    users[username] = User(username, password, role)
        return users