import tkinter as tk
from tkinter import messagebox
from database import create_contact_query

def submit_form():
    # Access the global variables for the form fields
    global entry_name, entry_email, entry_subject, text_message

    # Get values from the form
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    subject = entry_subject.get().strip()
    message = text_message.get("1.0", tk.END).strip()

    # Validate the form
    if not all([name, email, subject, message]):
        messagebox.showerror("Error", "All fields are required!")
        return

    # Save the query to the database
    create_contact_query(name, email, subject, message)
    messagebox.showinfo("Success", "Your query has been submitted!")
    root.destroy()

def create_contact_window():
    global entry_name, entry_email, entry_subject, text_message, root

    root = tk.Tk()
    root.title("Contact Us")
    root.geometry("500x400")
    root.iconbitmap("contact.ico")

    # Name
    tk.Label(root, text="Name:").pack(pady=5)
    entry_name = tk.Entry(root, width=40)
    entry_name.pack(pady=5)

    # Email
    tk.Label(root, text="Email:").pack(pady=5)
    entry_email = tk.Entry(root, width=40)
    entry_email.pack(pady=5)

    # Subject
    tk.Label(root, text="Subject:").pack(pady=5)
    entry_subject = tk.Entry(root, width=40)
    entry_subject.pack(pady=5)

    # Message
    tk.Label(root, text="Message:").pack(pady=5)
    text_message = tk.Text(root, width=40, height=8)
    text_message.pack(pady=5)

    # Submit Button
    tk.Button(root, text="Submit", command=submit_form).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_contact_window()