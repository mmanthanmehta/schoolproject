import mysql.connector
from datetime import datetime

# Connect to MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="admin",
    password="admin",
    database="bookstore"
)

cursor = db.cursor()

# Check if tables exist
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()

if len(tables) == 0:  # If no tables exist, create them
    # SQL code to create tables
    sql_commands = """
    CREATE TABLE books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        author VARCHAR(255),
        price FLOAT,
        quantity INT
    );

    CREATE TABLE customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255)
    );

    CREATE TABLE orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_id INT,
        book_id INT,
        quantity INT,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    );
    """

    # Execute SQL commands
    try:
        cursor.execute(sql_commands, multi=True)
        db.commit()
        print("Tables created successfully")
    except mysql.connector.Error as err:
        print("Error:", err)
else:
    print("Tables already exist")

# Function to add a book to the database
def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    price = float(input("Enter the price of the book: "))
    quantity = int(input("Enter the quantity of the book: "))
    
    sql = "INSERT INTO books (title, author, price, quantity) VALUES (%s, %s, %s, %s)"
    val = (title, author, price, quantity)
    cursor.execute(sql, val)
    db.commit()
    print("Book added successfully")

# Function to add a customer to the database
def add_customer():
    name = input("Enter the name of the customer: ")
    email = input("Enter the email of the customer: ")
    
    sql = "INSERT INTO customers (name, email) VALUES (%s, %s)"
    val = (name, email)
    cursor.execute(sql, val)
    db.commit()
    print("Customer added successfully")

# Function to list all books
def list_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    for book in books:
        print(book)

# Function to make an order
def make_order():
    customer_id = int(input("Enter the customer ID: "))
    
    # Check if the customer exists
    cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
    customer = cursor.fetchone()
    if customer is None:
        print("Error: Customer does not exist.")
        return

    book_id = int(input("Enter the book ID: "))
    quantity = int(input("Enter the quantity: "))
    
    sql = "INSERT INTO orders (customer_id, book_id, quantity) VALUES (%s, %s, %s)"
    val = (customer_id, book_id, quantity)
    cursor.execute(sql, val)
    db.commit()
    print("Order placed successfully")


# Function to list orders by customer
def list_orders_by_customer():
    customer_id = int(input("Enter the customer ID: "))
    sql = """
        SELECT orders.id, customers.name, books.title, orders.quantity, orders.order_date
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        JOIN books ON orders.book_id = books.id
        WHERE orders.customer_id = %s
    """
    val = (customer_id,)
    cursor.execute(sql, val)
    orders = cursor.fetchall()
    print("\nOrders for Customer ID :",{customer_id})
    print("------------------------------------")
    for order in orders:
        order_id, customer_name, book_title, quantity, order_date = order
        # Check if order_date is None
        if order_date is None:
            formatted_date = "N/A"
        else:
            # Formatting the order_date
            formatted_date = order_date.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Order ID: {order_id}, Customer: {customer_name}, Book: {book_title}, Quantity: {quantity}, Order Date: {formatted_date}")


# ASCII Art for the welcome message
# welcome_msg = """
# H   H  AAAAA  N   N  SSSSS  III  K   K  AAAAA
# H   H  A   A  NN  N  S       I   K  K   A   A
# HHHHH  AAAAA  N N N  SSSSS   I   KKK    AAAAA
# H   H  A   A  N  NN      S   I   K  K   A   A
# H   H  A   A  N   N  SSSSS  III  K   K  A   A
# """
welcome_msg = """
   ___              _        ___  _  _   
  | _ \  ___  ___  | |_     | _ \| || |  
  |  _/ / -_)(_-<  |  _|    |   /| __ |  
  |_|   \___|/__/_  \__|___ |_|_\ |_||_|  
   ___  ___ _ _  \/  _ _ / __|___ ____   
  / __|/ _ \ '_| | | | | | (__|_ / _  |  
  \__ \  _/ | | | | |_|_|_|\___/__\__,_|  
  |___/\___|_| |_|_|\___|___|___|_|      
"""

# Main loop
while True:
    print("\n" + welcome_msg)
    print("Main Menu:")
    print("1. Add Book")
    print("2. Add Customer")
    print("3. List Books")
    print("4. Make Order")
    print("5. List Orders by Customer")
    print("6. Exit")
    
    choice = input("Enter your choice (1-6): ")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        add_customer()
    elif choice == "3":
        list_books()
    elif choice == "4":
        make_order()
    elif choice == "5":
        list_orders_by_customer()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
        
db.close()
