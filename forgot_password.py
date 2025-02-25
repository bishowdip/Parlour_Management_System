# forgot_password.py
import tkinter as tk
from tkinter import messagebox
from database import get_user, update_password  # Ensure update_password is imported

def reset_password():
    username = username_entry.get()
    security_answer = security_answer_entry.get()
    new_password = new_password_entry.get()

    user = get_user(username)
    if not user:
        messagebox.showerror("Error", "Username not found!")
        return

    if security_answer != user[5]:  # Verify security answer
        messagebox.showerror("Error", "Incorrect security answer!")
        return

    # Update password
    update_password(username, new_password)
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