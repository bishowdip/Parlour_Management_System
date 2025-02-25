# contact.py
import tkinter as tk
from tkinter import messagebox

def submit_form():
    name = entry_name.get()
    email = entry_email.get()
    message = entry_message.get("1.0", "end-1c")  # Get text from the Text widget
    phone = entry_phone.get()

    if not name or not email or not message or not phone:
        messagebox.showwarning("Input Error", "All fields are required!")
    else:
        # In a real-world application, you might send the form data to a server or store it
        messagebox.showinfo("Confirmation", f"Thank you for reaching out, {name}!\nYour message has been submitted.")

def create_contact_window():
    root = tk.Tk()
    root.title("Contact Us")
    root.geometry("500x600")
    root.iconbitmap("contact.ico")

    # Add a header label
    header_label = tk.Label(root, text="Contact Us", font=("Arial", 20, "bold"))
    header_label.pack(pady=20)

    # Create the labels and entry fields for the form
    label_name = tk.Label(root, text="Name:")
    label_name.pack(pady=5)
    entry_name = tk.Entry(root, width=40)
    entry_name.pack(pady=5)

    label_email = tk.Label(root, text="Email:")
    label_email.pack(pady=5)
    entry_email = tk.Entry(root, width=40)
    entry_email.pack(pady=5)

    label_phone = tk.Label(root, text="Phone Number:")
    label_phone.pack(pady=5)
    entry_phone = tk.Entry(root, width=40)
    entry_phone.pack(pady=5)

    label_message = tk.Label(root, text="Message:")
    label_message.pack(pady=5)
    entry_message = tk.Text(root, height=6, width=40)
    entry_message.pack(pady=5)

    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=submit_form)
    submit_button.pack(pady=10)

    # Display the official contact information (Email and Phone)
    contact_info_frame = tk.Frame(root)
    contact_info_frame.pack(pady=15)

    label_contact_email = tk.Label(contact_info_frame, text="Official Email: beautybliss@gmail.com", font=("Arial", 12))
    label_contact_email.pack()

    label_contact_phone = tk.Label(contact_info_frame, text="Official Phone: +9779876543210", font=("Arial", 12))
    label_contact_phone.pack()

    root.mainloop()

if __name__ == "__main__":
    create_contact_window()