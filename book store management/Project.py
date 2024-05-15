import mysql.connector
import random
import string

def create_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="jayesh",
        database="jayeshsharma"
    )
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserVault (
            username VARCHAR(255),
            password VARCHAR(255),
            `token` VARCHAR(6)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notes (
            username VARCHAR(255),
            note TEXT
        )
    """)

def register(conn):
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    key = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=6))
    cursor = conn.cursor()
    cursor.execute("INSERT INTO UserVault (username, password, `key`) VALUES (%s, %s, %s)", (username, password, key))
    conn.commit()
    print(f"Your key is: {key}")

def login(conn):
    method = input("Enter '1' to login with username and password, '2' to login with key: ")
    cursor = conn.cursor()
    if method == '1':
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        cursor.execute("SELECT * FROM UserVault WHERE username=%s AND password=%s", (username, password))
    else:
        key = input("Enter your key: ")
        cursor.execute("SELECT * FROM UserVault WHERE `key`=%s", (key,))
    result = cursor.fetchone()
    if result:
        print("Login successful!")
        return result[0]
    else:
        print("Login failed!")
        return None

def notepad(conn, username):
    while True:
        print("1. Write Note\n2. View Notes\n3. Edit Note\n4. Logout")
        choice = input("Enter your choice: ")
        cursor = conn.cursor()
        if choice == '1':
            note = input("Enter your note: ")
            cursor.execute("INSERT INTO Notes (username, note) VALUES (%s, %s)", (username, note))
            conn.commit()
        elif choice == '2':
            cursor.execute("SELECT note FROM Notes WHERE username=%s", (username,))
            notes = cursor.fetchall()
            for i, note in enumerate(notes):
                print(f"Note {i+1}: {note[0]}")
        elif choice == '3':
            cursor.execute("SELECT note FROM Notes WHERE username=%s", (username,))
            notes = cursor.fetchall()
            for i, note in enumerate(notes):
                print(f"Note {i+1}: {note[0]}")
            note_number = int(input("Enter the number of the note you want to edit: ")) - 1
            new_note = input("Enter the new note: ")
            cursor.execute("UPDATE Notes SET note=%s WHERE username=%s AND note=%s", (new_note, username, notes[note_number][0]))
            conn.commit()
        else:
            break

def main():
    conn = create_connection()
    create_table(conn)
    while True:
        print("1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register(conn)
        elif choice == '2':
            username = login(conn)
            if username:
                notepad(conn, username)
        else:
            break

if __name__ == "__main__":
    main()
