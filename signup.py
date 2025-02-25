import tkinter as tk
from tkinter import messagebox
from database import create_user, get_user
import hashlib  # Import hashlib for password hashing

def signup():
    name = name_entry.get()
    email = email_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    security_answer = security_answer_entry.get()
    user_role = role_var.get()  # Get the selected role from the RadioButton

    if not all([name, email, username, password, security_answer]):
        messagebox.showerror("Error", "All fields are required!")
        return

    if get_user(username):
        messagebox.showerror("Error", "Username already exists!")
        return

    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    # Save user to database
    create_user(username, password_hash, user_role, name, email, security_answer)
    messagebox.showinfo("Success", "Signup successful! Please login.")
    back_to_login()

def back_to_login():
    root.destroy()  # Close signup window
    import login
    login.create_login_window()

def create_signup_window():
    global name_entry, email_entry, username_entry, password_entry, security_answer_entry, role_var, root

    root = tk.Tk()
    root.title("Sign Up")
    root.geometry("400x500")  # Increased height to accommodate the RadioButton
    root.iconbitmap("sign_up.ico")

    # Name
    tk.Label(root, text="Full Name:").pack(pady=5)
    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    # Email
    tk.Label(root, text="Email:").pack(pady=5)
    email_entry = tk.Entry(root)
    email_entry.pack(pady=5)

    # Username
    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    # Password
    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    # Security Question
    tk.Label(root, text="Security Question: What is your pet's name?").pack(pady=5)
    security_answer_entry = tk.Entry(root)
    security_answer_entry.pack(pady=5)

    # Role Selection (RadioButton)
    tk.Label(root, text="Select Role:").pack(pady=5)
    role_var = tk.StringVar(value="customer")  # Default role is "customer"
    tk.Radiobutton(root, text="Customer", variable=role_var, value="customer").pack(pady=2)
    tk.Radiobutton(root, text="Employee", variable=role_var, value="employee").pack(pady=2)

    # Signup Button
    tk.Button(root, text="Sign Up", command=signup).pack(pady=10)

    # Back to Login Button
    tk.Button(root, text="Back to Login", command=back_to_login).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_signup_window()