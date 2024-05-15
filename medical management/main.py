import mysql.connector
from datetime import datetime

# Connect to MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="admin1",
    password="admin",
    database="medical"
)
# Create a cursor
cursor = db.cursor()

# Create patients table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT,
        gender VARCHAR(10),
        bed_number INT,
        admission_time DATETIME
    )
""")

# Function to add a new patient
def add_patient(name, age, gender):
    sql = "INSERT INTO patients (name, age, gender) VALUES (%s, %s, %s)"
    val = (name, age, gender)
    cursor.execute(sql, val)
    db.commit()
    return cursor.lastrowid

# Function to update patient information
def update_patient(id, name, age, gender):
    # Retrieve old data
    old_data = get_patient(id)
    
    # Update patient information
    sql = "UPDATE patients SET name = %s, age = %s, gender = %s WHERE id = %s"
    val = (name, age, gender, id)
    cursor.execute(sql, val)
    db.commit()
    
    # Retrieve new data
    new_data = get_patient(id)
    
    return old_data, new_data

# Function to delete a patient
def delete_patient(id):
    # Retrieve patient data before deletion
    patient_data = get_patient(id)
    
    sql = "DELETE FROM patients WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    db.commit()
    
    return patient_data

# Function to fetch patient data by ID
def get_patient(id):
    sql = "SELECT * FROM patients WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    return cursor.fetchone()

# Function to list patients with their IDs and names
def list_patients():
    sql = "SELECT id, name FROM patients"
    cursor.execute(sql)
    patients = cursor.fetchall()
    return patients

# Function to admit a patient
def admit_patient(id):
    # Get current date and time
    now = datetime.now()
    admission_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # Update patient's admission time
    sql = "UPDATE patients SET admission_time = %s WHERE id = %s"
    val = (admission_time, id)
    cursor.execute(sql, val)
    db.commit()
    
    return admission_time


def list_patients_with_ever():
    patients = list_patients()
    print("\nList of Patients:")
    for patient in patients:
            print("ID:", patient[0], "Name:", patient[1])

# Loop for user interaction
while True:
    print("\nChoose an action:")
    print("1. Add patient")
    print("2. Update patient")
    print("3. Delete patient")
    print("4. Admit patient")
    print("5. List patients")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter patient name: ")
        age = input("Enter patient age: ")
        gender = input("Enter patient gender: ")
        add_patient(name, age, gender)
        print("Patient added successfully!")

    elif choice == "2":
        list_patients_with_ever()
        id = input("Enter patient ID to update: ")
        name = input("Enter new name: ")
        age = input("Enter new age: ")
        gender = input("Enter new gender: ")
        old_data, new_data = update_patient(id, name, age, gender)
        print("Patient information updated successfully!")
        print("Old Data:", old_data)
        print("New Data:", new_data)


    elif choice == "3":
        list_patients_with_ever()
        id = input("Enter patient ID to delete: ")
        patient_data = delete_patient(id)
        print("Patient deleted successfully!")
        print("Deleted Patient Data:", patient_data)

    elif choice == "4":
        list_patients_with_ever()
        ids = input("Enter patient ID to admit: ")
        admission_time = admit_patient(ids)
        print("Patient admitted successfully at:", admission_time)
    elif choice == "5":
        patients = list_patients()
        print("\nList of Patients:")
        for patient in patients:
            print("ID:", patient[0], "Name:", patient[1])

    elif choice == "6":
        break

    else:
        print("Invalid choice. Please enter a valid option.")

# Close connection
cursor.close()
db.close()