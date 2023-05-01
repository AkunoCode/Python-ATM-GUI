import mysql.connector
from mysql.connector import Error
from DATABASE_CONFIG import *

class ATM_Manager():

    def __init__(self) -> None:
        """Initialize the database connection"""
        self.db = mysql.connector.connect(
            host=dbhost,
            user=dbuser,
            password=dbpass,
            database=dbname
        )
        self.cursor = self.db.cursor()

    def register_users(self, userID, surname, fstname, homeadd, phonenum):
        """Register a new user to the database"""
        try:
            query = "INSERT INTO users (userID, surname, fstname, homeadd, phonenum) VALUES (%s, %s, %s, %s, %s)"
            vars = (userID, surname, fstname, homeadd, phonenum)
            self.cursor.execute(query, vars)
            self.db.commit()
        except Error as e:
            print(f"Failed to insert record into MySQL table {e}")

    def register_account(self, account_no, acctype, userID, balance, withdraw_limit, withdraw_freq):
        """Register a new account to the database"""
        try:
            query = "INSERT INTO accounts (account_no, acctype, userID, balance, withdraw_limit, withdraw_freq) VALUES (%s, %s, %s, %s, %s, %s)"
            vars = (account_no, acctype, userID, balance, withdraw_limit, withdraw_freq)
            self.cursor.execute(query, vars)
            self.db.commit()
        except Error as e:
            print(f"Failed to insert record into MySQL table {e}")

    def view_one(self, table, condition, value):
        """View a record from a table"""
        try:
            query = f"SELECT * FROM {table} WHERE {condition} = {value}"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        except Error as e:
            print(f"Failed to select record from MySQL table {e}")

    def view_user(self, userID):
        """View a user's details by calling view_one()"""
        return self.view_one("users", "userID", userID)
        
    def view_account(self, account_no):
        """View an account's details by calling view_one()"""
        return self.view_one("accounts", "account_no", account_no)
    
    def view_balance(self, account_no):
        """View an account's balance"""
        return self.view_one("accounts", "account_no", account_no)[3]
        
    def view_all_transactions(self, account_no):
        """View all transactions of an account"""
        try:
            query = f"SELECT * FROM transactions WHERE account_no = {account_no}"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Failed to select record from MySQL table {e}")
    
    def view_day_transactions(self, account_no):
        """View all transactions of an account within the day"""
        try:
            query = f"SELECT * FROM transactions WHERE account_no = {account_no} AND trans_date = CURDATE()"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Failed to select record from MySQL table {e}")

    def withdraw(self, account_no, amount):
        """Check first if the amount to be withdrawn is within the limit and frequency"""
        
        # Get the transaction history of the account within the day and sum up the withdrawals
        transactions = self.view_day_transactions(account_no)
        total_withdrawals_amount = 0
        total_withdrawals_freq = 0
        for transaction in transactions:
            if transaction[3] == "Withdraw":
                total_withdrawals_amount += transaction[4]
                total_withdrawals_freq += 1

        # Check if the amount to be withdrawn is within the limit and frequency
        if amount > self.view_account(account_no)[3]:
            return "Insufficient funds."
        elif total_withdrawals_freq > self.view_account(account_no)[5]:
            return "Exceeded withdrawal frequency for today."
        elif total_withdrawals_amount > self.view_account(account_no)[4]:
            return "Exceeded withdrawal limit for today."
        elif total_withdrawals_amount + amount > self.view_account(account_no)[4]:
            return "Amount will exceed withdrawal limit for today."
        else:
            try:
                # Updating the balance of the account
                query = f"UPDATE accounts SET balance = balance - {amount} WHERE account_no = {account_no}"
                self.cursor.execute(query)
                self.db.commit()
                
                # Adding the transaction into the transaction history
                query = "INSERT INTO transactions (account_no, trans_date, transaction_type, amount) VALUES (%s, CURDATE(), %s, %s)"
                vars = (account_no, "Withdraw", amount)
                self.cursor.execute(query, vars)
                self.db.commit()
                
                return "Done"
            except Error as e:
                print(f"Failed to update record in MySQL table {e}")
    
    def deposit(self, account_no, amount):
        """Deposit money into an account and add into the transaction history"""
        try:
            # Updating the balance of the account
            query = f"UPDATE accounts SET balance = balance + {amount} WHERE account_no = {account_no}"
            self.cursor.execute(query)
            self.db.commit()
            
            # Adding the transaction into the transaction history
            query = "INSERT INTO transactions (account_no, trans_date, trans_type, amount) VALUES (%s, CURDATE(), %s, %s)"
            vars = (account_no, "Deposit", amount)
            self.cursor.execute(query, vars)
            self.db.commit()
            
            return "Done"
        except Error as e:
            print(f"Failed to update record in MySQL table {e}")       