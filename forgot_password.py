import tkinter as tk
from tkinter import messagebox
from database import get_user, update_password
import hashlib  # For password hashing

def reset_password():
    username = username_entry.get().strip()
    security_answer = security_answer_entry.get().strip()
    new_password = new_password_entry.get().strip()

    if not username or not security_answer or not new_password:
        messagebox.showerror("Error", "All fields are required!")
        return

    user = get_user(username)
    if not user:
        messagebox.showerror("Error", "Username not found!")
        return

    # Debugging: Print the security answers
    print(f"Database Security Answer: {user['security_answer']}")
    print(f"Entered Security Answer: {security_answer}")

    if security_answer != user["security_answer"]:  # Verify security answer
        messagebox.showerror("Error", "Incorrect security answer!")
        return

    # Hashed the new password
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()

    # to Update password
    update_password(username, password_hash)
    messagebox.showinfo("Success", "Password reset successful! Please login.")
    back_to_login()

def back_to_login():
    root.destroy()  # Close forgot password window
    import login
    login.create_login_window()

def create_forgot_password_window():
    global username_entry, security_answer_entry, new_password_entry, root

    root = tk.Tk()
    root.title("Forgot Password")
    root.geometry("400x300")
    root.iconbitmap("forget.ico")

    # Username
    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    # Security Question
    tk.Label(root, text="Security Question: What is your pet's name?").pack(pady=5)
    security_answer_entry = tk.Entry(root)
    security_answer_entry.pack(pady=5)

    # New Password
    tk.Label(root, text="New Password:").pack(pady=5)
    new_password_entry = tk.Entry(root, show="*")
    new_password_entry.pack(pady=5)

    # Reset Password Button
    tk.Button(root, text="Reset Password", command=reset_password).pack(pady=10)

    # Back to Login Button
    tk.Button(root, text="Back to Login", command=back_to_login).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_forgot_password_window()