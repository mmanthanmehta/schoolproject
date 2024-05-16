import mysql.connector
from getpass import getpass
from decimal import Decimal

# Connect to MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="admin2",
            password="admin",
            database="atm"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error:", err)
        return None

# Create table if not exists
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_number VARCHAR(20) UNIQUE,
            pin VARCHAR(4),
            balance DECIMAL(10, 2)
        )
    """)
    conn.commit()

# Insert a new account if it does not exist
def insert_account(conn, account_number, pin, balance):
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM accounts WHERE account_number = %s"
    cursor.execute(query, (account_number,))
    count = cursor.fetchone()[0]
    if count == 0:
        query = "INSERT INTO accounts (account_number, pin, balance) VALUES (%s, %s, %s)"
        cursor.execute(query, (account_number, pin, balance))
        conn.commit()
        print("Account created successfully.")
    else:
        print("Account with this account number already exists.")

# Function to validate PIN
def validate_pin(conn, acc_num, pin):
    cursor = conn.cursor()
    query = "SELECT * FROM accounts WHERE account_number = %s AND pin = %s"
    cursor.execute(query, (acc_num, pin))
    return cursor.fetchone()

# Function to check balance
def check_balance(conn, acc_num):
    cursor = conn.cursor()
    query = "SELECT balance FROM accounts WHERE account_number = %s"
    cursor.execute(query, (acc_num,))
    return cursor.fetchone()[0]

# Function to withdraw money
def withdraw(conn, acc_num, amount):
    cursor = conn.cursor()
    current_balance = Decimal(check_balance(conn, acc_num))
    amount = Decimal(str(amount))
    if current_balance >= amount:
        new_balance = current_balance - amount
        query = "UPDATE accounts SET balance = %s WHERE account_number = %s"
        cursor.execute(query, (new_balance, acc_num))
        conn.commit()
        return True
    else:
        return False

# Function to deposit money
def deposit(conn, acc_num, amount):
    cursor = conn.cursor()
    current_balance = Decimal(check_balance(conn, acc_num))
    amount = Decimal(str(amount))
    new_balance = current_balance + amount
    query = "UPDATE accounts SET balance = %s WHERE account_number = %s"
    cursor.execute(query, (new_balance, acc_num))
    conn.commit()

# Main function
def main():
    conn = connect_to_database()
    if conn:
        print("Welcome to the Bank")
        create_table(conn)

        while True:
            print("\n1. Create Account\n2. Login\n3. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                account_number = input("Enter your account number: ")
                pin = getpass("Create your 4-digit PIN: ")
                balance = float(input("Enter initial balance: "))
                insert_account(conn, account_number, pin, balance)
            elif choice == "2":
                acc_num = input("Enter account number: ")
                pin = getpass("Enter PIN: ")
                user = validate_pin(conn, acc_num, pin)
                if user:
                    print("Welcome, {}!".format(user[1]))  # Assuming the second column is the user's name
                    while True:
                        print("\n1. Check Balance\n2. Withdraw\n3. Deposit\n4. Logout")
                        choice = input("Enter your choice: ")
                        if choice == "1":
                            print("Your balance is:", check_balance(conn, acc_num))
                        elif choice == "2":
                            amount = float(input("Enter amount to withdraw: "))
                            if withdraw(conn, acc_num, amount):
                                print("Amount withdrawn successfully")
                            else:
                                print("Insufficient funds")
                        elif choice == "3":
                            amount = float(input("Enter amount to deposit: "))
                            deposit(conn, acc_num, amount)
                            print("Amount deposited successfully")
                        elif choice == "4":
                            break
                        else:
                            print("Invalid choice")
                else:
                    print("Invalid account number or PIN. Please try again.")
            elif choice == "3":
                break
            else:
                print("Invalid choice")

        conn.close()
        print("\nThank you for using the Bank.")

if __name__ == "__main__":
    main()