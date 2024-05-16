import mysql.connector

# Connect to MySQL
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="admin3",
    password="admin",
    database="bank"
)

# Create necessary tables if not exists
def create_tables():
    cursor = db_connection.cursor()
    # Create accounts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            balance DECIMAL(10, 2) NOT NULL
        )
    """)
    # Create loans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    # Create fds table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fds (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            duration_months INT NOT NULL,
            interest_rate DECIMAL(5, 2) NOT NULL,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    # Create rds table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rds (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT NOT NULL,
            installment_amount DECIMAL(10, 2) NOT NULL,
            duration_months INT NOT NULL,
            interest_rate DECIMAL(5, 2) NOT NULL,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    db_connection.commit()
    cursor.close()
    
# Function to create a new account
def create_account(name, balance):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", (name, balance))
    db_connection.commit()
    cursor.close()
    print("Account created successfully.")

# Function to deposit money
def deposit(account_id, amount):
    cursor = db_connection.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))
    db_connection.commit()
    cursor.close()
    print("Deposit successful.")

# Function to withdraw money
def withdraw(account_id, amount):
    cursor = db_connection.cursor()
    cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))
    db_connection.commit()
    cursor.close()
    print("Withdrawal successful.")

# Function to check balance
def check_balance(account_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    balance = cursor.fetchone()[0]
    cursor.close()
    print("Your balance:", balance)

# Function to apply for a loan
def apply_loan(account_id, amount):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO loans (account_id, amount) VALUES (%s, %s)", (account_id, amount))
    db_connection.commit()
    cursor.close()
    
    # Deduct the loan amount from the bank's balance
    cursor = db_connection.cursor()
    cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = 1", (amount,))
    db_connection.commit()
    cursor.close()
    
    print("Loan of", amount, "granted.")

# Function to create a fixed deposit
def create_fd(account_id, amount, duration_months, interest_rate):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO fds (account_id, amount, duration_months, interest_rate) VALUES (%s, %s, %s, %s)",
                   (account_id, amount, duration_months, interest_rate))
    db_connection.commit()
    cursor.close()
    
    # Add the FD amount to the bank's balance
    cursor = db_connection.cursor()
    cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = 1", (amount,))
    db_connection.commit()
    cursor.close()
    
    print("Fixed deposit created successfully.")

# Function to create a recurring deposit
def create_rd(account_id, installment_amount, duration_months, interest_rate):
    total_amount = installment_amount * duration_months
    
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO rds (account_id, installment_amount, duration_months, interest_rate) VALUES (%s, %s, %s, %s)",
                   (account_id, installment_amount, duration_months, interest_rate))
    db_connection.commit()
    cursor.close()
    
    # Add the total RD amount to the bank's balance
    cursor = db_connection.cursor()
    cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = 1", (total_amount,))
    db_connection.commit()
    cursor.close()
    print("Recurring deposit created successfully.")


# Function to display all user IDs and names
def display_accounts():
    cursor = db_connection.cursor()
    cursor.execute("SELECT id, name FROM accounts")
    accounts = cursor.fetchall()
    cursor.close()
    print("\nExisting Users:")
    for account in accounts:
        print(f"ID: {account[0]}, Name: {account[1]}")

# Main menu
def main():
    create_tables()
    
    while True:
        print("\nBank Management System")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Apply for Loan")
        print("6. Create Fixed Deposit")
        print("7. Create Recurring Deposit")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            balance = float(input("Enter initial balance: "))
            create_account(name, balance)
        elif choice == '2':
            display_accounts()
            account_id = int(input("Enter account id: "))
            amount = float(input("Enter amount to deposit: "))
            deposit(account_id, amount)
        elif choice == '3':
            display_accounts()
            account_id = int(input("Enter account id: "))
            amount = float(input("Enter amount to withdraw: "))
            withdraw(account_id, amount)
        elif choice == '4':
            display_accounts()
            account_id = int(input("Enter account id: "))
            check_balance(account_id)
        elif choice == '5':
            display_accounts()
            account_id = int(input("Enter account id: "))
            amount = float(input("Enter loan amount: "))
            apply_loan(account_id, amount)
        elif choice == '6':
            display_accounts()
            account_id = int(input("Enter account id: "))
            amount = float(input("Enter FD amount: "))
            duration_months = int(input("Enter FD duration in months: "))
            interest_rate = float(input("Enter FD interest rate (annual): "))
            create_fd(account_id, amount, duration_months, interest_rate)
        elif choice == '7':
            display_accounts()
            account_id = int(input("Enter account id: "))
            installment_amount = float(input("Enter RD installment amount: "))
            duration_months = int(input("Enter RD duration in months: "))
            interest_rate = float(input("Enter RD interest rate (annual): "))
            create_rd(account_id, installment_amount, duration_months, interest_rate)
        elif choice == '8':
            print("Thank you for using our system.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()