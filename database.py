# database.py
import sqlite3
from datetime import datetime

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect('salon.db')
    conn.row_factory = sqlite3.Row  # Allow column access by name
    return conn

# Function to get a user by username
def get_user(username):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user  # Returns user tuple if found, otherwise None

# Function to create tables
def create_tables():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY,
                      username TEXT UNIQUE,
                      password_hash TEXT,
                      role TEXT,
                      name TEXT,
                      email TEXT,
                      security_answer TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS contact_queries (
                      id INTEGER PRIMARY KEY,
                      name TEXT,
                      email TEXT,
                      subject TEXT,
                      message TEXT,
                      submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # Create the services table
    cursor.execute('''CREATE TABLE IF NOT EXISTS services (
                      id INTEGER PRIMARY KEY,
                      name TEXT UNIQUE,
                      price REAL)''')

    # Create the appointments table
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                      id INTEGER PRIMARY KEY,
                      customer_name TEXT,
                      service_id INTEGER,
                      contact TEXT,
                      appointment_date DATE,
                      appointment_time TIME,
                      status TEXT DEFAULT 'scheduled',
                      FOREIGN KEY(service_id) REFERENCES services(id))''')

    # Create the transactions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                      id INTEGER PRIMARY KEY,
                      customer_name TEXT,
                      total_amount REAL,
                      transaction_date DATETIME,
                      services_used TEXT)''')

    # Insert default services if they don't exist
    default_services = [
        ('Haircut', 200),
        ('Facial', 1000),
        ('Manicure', 1500),
        ('Pedicure', 1200),
        ('Massage', 2000),
        ('Bridal Makeup', 8000),
        ('Eyelashes', 1500),
        ('Nail Extension', 1200)
    ]
    cursor.executemany('''INSERT OR IGNORE INTO services (name, price)
                          VALUES (?, ?)''', default_services)

    conn.commit()
    conn.close()

# Function to drop the users table (for testing purposes)
def drop_users_table():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    conn.close()

# Function to create a new user
def create_user(username, password_hash, role, name, email, security_answer):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO users (username, password_hash, role, name, email, security_answer)
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (username, password_hash, role, name, email, security_answer))
        conn.commit()
        print(f"User '{username}' created successfully!")  # Debugging
    except sqlite3.IntegrityError as e:
        print(f"Error creating user: {e}")  # Debugging
    finally:
        conn.close()

# Function to check the schema of the users table (for testing purposes)
def check_users_table_schema():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    for column in columns:
        print(column)
    conn.close()

# Function to save a contact query
def create_contact_query(name, email, subject, message):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO contact_queries (name, email, subject, message)
                          VALUES (?, ?, ?, ?)''',
                       (name, email, subject, message))
        conn.commit()
        print("Contact query saved successfully!")
    except sqlite3.Error as e:
        print(f"Error saving query: {e}")
    finally:
        conn.close()

# Function to get all contact queries (for employees)
def get_all_contact_queries():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contact_queries ORDER BY submitted_at DESC")
    queries = cursor.fetchall()
    conn.close()
    return queries


# Function to get all services
def get_services():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()
    return services

# Function to create a new appointment
def create_appointment(customer_name, service_id, contact, appointment_date, appointment_time):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO appointments (customer_name, service_id, contact, appointment_date, appointment_time)
                          VALUES (?, ?, ?, ?, ?)''',
                       (customer_name, service_id, contact, appointment_date, appointment_time))
        conn.commit()
        print(f"Appointment for '{customer_name}' created successfully!")  # Debugging
    except sqlite3.Error as e:
        print(f"Error creating appointment: {e}")  # Debugging
    finally:
        conn.close()

# Function to create a new transaction
def create_transaction(customer_name, total_amount, services_used):
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO transactions (customer_name, total_amount, transaction_date, services_used)
                          VALUES (?, ?, ?, ?)''',
                       (customer_name, total_amount, datetime.now(), services_used))
        conn.commit()
        print(f"Transaction for '{customer_name}' created successfully!")  # Debugging
    except sqlite3.Error as e:
        print(f"Error creating transaction: {e}")  # Debugging
    finally:
        conn.close()

# Function to get all users
def get_all_users():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Function to get all appointments
def get_all_appointments():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    conn.close()
    return appointments

# Function to get all transactions
def get_all_transactions():
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def update_password(username, new_password):
    """Update the password for a user."""
    conn = sqlite3.connect('salon.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''UPDATE users SET password_hash = ? WHERE username = ?''',
                       (new_password, username))
        conn.commit()
        print(f"Password updated for user '{username}'.")  # Debugging
    except sqlite3.Error as e:
        print(f"Error updating password: {e}")  # Debugging
    finally:
        conn.close()



def get_all_appointments():
    """Get all appointments with service names."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, s.name as service_name 
            FROM appointments a
            JOIN services s ON a.service_id = s.id
        ''')
        return cursor.fetchall()
    finally:
        conn.close()

def delete_appointment(appointment_id):
    """Delete an appointment by ID."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting appointment: {e}")
    finally:
        conn.close()
