import tkinter as tk
from tkinter import messagebox
from database import get_user
from database import create_tables
import hashlib  # Import hashlib for password hashing
from home import create_home_window  # Import the create_home_window function

def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        toggle_button.config(text="👁")  # Open eye
    else:
        password_entry.config(show="*")
        toggle_button.config(text="👁‍🗨")  # Closed eye

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    user = get_user(username)
    if user:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user["password_hash"] == password_hash:  # Access using dictionary key
            messagebox.showinfo("Success", "Login successful!")
            root.destroy()
            user_role = user["role"]  # Access using dictionary key
            home_root = tk.Tk()
            create_home_window(home_root, user_role=user_role)  # Use the imported function
            home_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid password")
    else:
        messagebox.showerror("Error", "User not found")

def open_signup():
    root.destroy()  # Close login window
    import signup
    signup.create_signup_window()

def open_forgot_password():
    root.destroy()  # Close login window
    import forgot_password
    forgot_password.create_forgot_password_window()

# Create login window
root = tk.Tk()
root.title("Login")
root.geometry("400x300")  # Initial size of the window
root.iconbitmap("login.ico")

# Set maximum size of the window
root.maxsize(800, 800)  # Maximum size of the window

# Add background image
background_image = tk.PhotoImage(file="login.png")
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.image = background_image  # Keep a reference to avoid garbage collection

# Username
tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Password
tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_frame = tk.Frame(root)
password_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")

password_entry = tk.Entry(password_frame, show="*", width=20)
password_entry.pack(side=tk.LEFT)

# Eye button to toggle password visibility
toggle_button = tk.Button(password_frame, text="👁‍🗨", command=toggle_password)
toggle_button.pack(side=tk.LEFT)

# Login Button
tk.Button(root, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)

# Signup Button
tk.Button(root, text="Sign Up", command=open_signup).grid(row=3, column=0, columnspan=2, pady=5)

# Forgot Password Button
tk.Button(root, text="Forgot Password", command=open_forgot_password).grid(row=4, column=0, columnspan=2, pady=5)

# Center the widgets in the window
for i in range(5):
    root.grid_rowconfigure(i, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

create_tables()

if __name__ == "__main__":
    root.mainloop()