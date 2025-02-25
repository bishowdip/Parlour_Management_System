# home.py
import tkinter as tk
import view_appointments
from PIL import Image, ImageTk

def create_home_window(root):
    root.title("Home")
    root.geometry("500x400")
    root.iconbitmap("logo.ico")
    

    tk.Label(root, text="Welcome to Salon Management System", font=("Arial", 16)).pack(pady=20)

    # Buttons for different features
    tk.Button(root, text="Services", command=open_services).pack(pady=10)  # New Services button
    tk.Button(root, text="Appointments", command=lambda: open_appointments(root)).pack(pady=10)  # Pass root as parent
    tk.Button(root, text="View Appointments", command=lambda: view_appointments.create_view_appointments_window(root)).pack(pady=10)
    tk.Button(root, text="Billing", command=open_billing).pack(pady=10)
    tk.Button(root, text="Contact US", command=open_contact).pack(pady=10)
    tk.Button(root, text="About Us", command=open_about).pack(pady=10)
    tk.Button(root, text="Logout", command=root.destroy).pack(pady=10)

def open_appointments(parent):  # Accept parent argument
    import appointment
    appointment.create_appointment_window(parent)  # Pass parent to the appointment window


def open_billing():
    import billing
    billing.create_billing_window()

def open_services():  # New function to open Services page
    import service
    service.create_service_window()

def open_contact():
    import Contact_Us
    Contact_Us.create_contact_window()


def open_about():
    import About_Us
    About_Us.create_about_window()

if __name__ == "__main__":
    root = tk.Tk()
    create_home_window(root)
    root.mainloop()