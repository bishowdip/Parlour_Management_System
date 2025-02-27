#appointment file
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from database import get_services, create_appointment, update_appointment

from database import get_services, create_appointment, update_appointment  # Import update_appointment

def book_appointment(name_entry, service_var, contact_entry, date_picker, time_var, window, appointment_id=None):
    name = name_entry.get()
    service = service_var.get()
    contact = contact_entry.get()
    appointment_date = date_picker.get_date().strftime("%Y-%m-%d")
    appointment_time = time_var.get()

    # to make contact exactly  10 digits only
    if len(contact) != 10 or not contact.isdigit():
        messagebox.showerror("Error", "Please enter a valid 10-digit contact number!")
        return

    if not all([name, service, contact, appointment_date, appointment_time]):
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    services = get_services()
    service_id = next((s[0] for s in services if s[1] == service), None)

    if not service_id:
        messagebox.showerror("Error", "Invalid service selected!")
        return

    if appointment_id:
        # Update existing appointment
        update_appointment(appointment_id, name, service_id, contact, appointment_date, appointment_time)
        messagebox.showinfo("Success", "Appointment has been updated successfully!")
    else:
        # Create new appointment
        create_appointment(name, service_id, contact, appointment_date, appointment_time)
        messagebox.showinfo("Success", "Appointment has been booked successfully! If you want to cancel the appointment, please contact us from contact us section. Thank you!")
    clear_fields(name_entry, contact_entry, service_var, time_var)
    window.destroy() 
    
 # Close the appointment window after booking or updating
def clear_fields(name_entry, contact_entry, service_var, time_var):
    name_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    service_var.set("")
    time_var.set("")

def create_appointment_window(parent, appointment_id=None, customer_name=None, contact=None, service_name=None, appointment_date=None, appointment_time=None, on_save=None):
    # Create a Toplevel window instead of Tk()
    appointment_window = tk.Toplevel(parent)
    appointment_window.title("Appointment Booking" if not appointment_id else "Edit Appointment")
    appointment_window.geometry("500x400")

    # Name
    tk.Label(appointment_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(appointment_window)
    name_entry.pack(pady=5)
    if customer_name:
        name_entry.insert(0, customer_name)
    

    # Service
    tk.Label(appointment_window, text="Service:").pack(pady=5)
    service_var = tk.StringVar(appointment_window)
    services = [s[1] for s in get_services()]
    service_dropdown = tk.OptionMenu(appointment_window, service_var, *services)
    service_dropdown.pack(pady=5)
    if service_name and service_name in services:
        service_var.set(service_name)
    else:
        service_var.set(services[0] if services else "") # Default to first service

    # Contact
    tk.Label(appointment_window, text="Contact:").pack(pady=5)
    contact_entry = tk.Entry(appointment_window, validate="key", validatecommand=(appointment_window.register(validate_contact), "%P"))
    contact_entry.pack(pady=5)
    if contact:
        contact_entry.insert(0, contact)


    # Date Picker (restrict past dates)
    tk.Label(appointment_window, text="Date:").pack(pady=5)
    date_picker = DateEntry(appointment_window, date_pattern="yyyy-mm-dd", mindate=datetime.today())
    date_picker.pack(pady=5)

    # Time Picker
    tk.Label(appointment_window, text="Time:").pack(pady=5)
    time_var = tk.StringVar(appointment_window)
    time_slots = generate_time_slots()
    time_dropdown = tk.OptionMenu(appointment_window, time_var, *time_slots)
    time_dropdown.pack(pady=5)
    time_var.set(time_slots[0] if time_slots else "")  # Default to first slot

    # Buttons
    tk.Button(
        appointment_window,
        text="Book Appointment" if not appointment_id else "Update Appointment",
        command=lambda: book_appointment(name_entry, service_var, contact_entry, date_picker, time_var, appointment_window, appointment_id)
    ).pack(pady=10)
    
    tk.Button(
        appointment_window,
        text="Clear",
        command=lambda: clear_fields(name_entry, contact_entry, service_var, time_var)
    ).pack(pady=5)
    

def validate_contact(contact):
    """Validates that the contact number is exactly 10 digits."""
    if len(contact) > 10:
        return False  # Reject input if length exceeds 10 digits
    return contact.isdigit()  # Accept only digits

def generate_time_slots():
    """Generate time slots from 9:00 AM to 6:00 PM with 1-hour intervals."""
    return [f"{hour:02d}:00" for hour in range(9, 19)]  # 09:00 to 18:00

# Add this block to allow running appointment.py directly
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main root window
    create_appointment_window(root, preselected_service="Haircut")
    root.mainloop()
