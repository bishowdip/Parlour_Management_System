import sqlite3
from datetime import datetime

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect('salon.db')
    conn.row_factory = sqlite3.Row  # Allow column access by name
    return conn

# Function to get a user by username
def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        # Convert the tuple to a dictionary
        user_dict = {
            'id': user[0],
            'username': user[1],
            'password_hash': user[2],
            'role': user[3],
            'name': user[4],
            'email': user[5],
            'security_answer': user[6]
        }
        return user_dict
    return None

def create_tables():
    conn = get_db_connection()
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

    # Create the services table
    cursor.execute('''CREATE TABLE IF NOT EXISTS services (
                      id INTEGER PRIMARY KEY,
                      name TEXT UNIQUE,
                      price REAL,
                      description TEXT)''')

    # Create the contact_queries table with status column
    cursor.execute('''CREATE TABLE IF NOT EXISTS contact_queries (
                      id INTEGER PRIMARY KEY,
                      name TEXT,
                      email TEXT,
                      subject TEXT,
                      message TEXT,
                      status TEXT DEFAULT 'Pending',  -- Add status column
                      submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')

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

    conn.commit()
    conn.close()


# Function to drop the users table (for testing purposes)
def drop_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    conn.close()

# Function to create a new user
def create_user(username, password_hash, role, name, email, security_answer):
    conn = get_db_connection()
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    for column in columns:
        print(column)
    conn.close()

# Function to save a contact query
def create_contact_query(name, email, subject, message):
    conn = get_db_connection()
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contact_queries ORDER BY submitted_at DESC")
    queries = cursor.fetchall()
    conn.close()
    return queries

# Function to get all services
def get_services():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()
    return services

# Function to create a new appointment
def create_appointment(customer_name, service_id, contact, appointment_date, appointment_time):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO appointments (customer_name, service_id, contact, appointment_date, appointment_time)
                          VALUES (?, ?, ?, ?, ?)''',
                       (customer_name, service_id, contact, appointment_date, appointment_time))
        conn.commit()
        print(f"Appointment for '{customer_name}' created successfully!")
    except sqlite3.Error as e:
        print(f"Error creating appointment: {e}")
    finally:
        conn.close()


# Function to create a new transaction
def create_transaction(customer_name, total_amount, services_used):
    conn = get_db_connection()
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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# Function to get all appointments
def get_all_appointments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            appointments.id, 
            appointments.customer_name, 
            appointments.contact, 
            services.name AS service_name, 
            appointments.appointment_date, 
            appointments.appointment_time, 
            appointments.status
        FROM appointments
        LEFT JOIN services ON appointments.service_id = services.id
    ''')
    appointments = cursor.fetchall()
    conn.close()
    return appointments

# Function to get all transactions
def get_all_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def update_password(username, new_password):
    """Update the password for a user."""
    conn = get_db_connection()
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

def update_appointment(appointment_id, customer_name, service_id, contact, appointment_date, appointment_time):
    """Update an existing appointment."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE appointments 
                          SET customer_name=?, service_id=?, contact=?, appointment_date=?, appointment_time=?
                          WHERE id=?''',
                       (customer_name, service_id, contact, appointment_date, appointment_time, appointment_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating appointment: {e}")
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

# Function to add a new service
def add_service(name, price, description):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO services (name, price, description)
                          VALUES (?, ?, ?)''',
                       (name, price, description))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding service: {e}")
    finally:
        conn.close()


# Function to get all services
def get_services():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    print("Fetched services:", services)  # Debug: Print fetched services
    conn.close()
    return services

# Function to delete a service
def delete_service(service_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting service: {e}")
    finally:
        conn.close()

# Update query status
def update_query_status(query_id, new_status):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''UPDATE contact_queries 
                          SET status = ?
                          WHERE id = ?''',
                       (new_status, query_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating query status: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    create_tables()
