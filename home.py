import tkinter as tk
import view_appointments
from view_query import view_queries  # Import view_queries function

def create_home_window(root, user_role="employee"):
    root.title("Home")
    root.geometry("500x400")
    root.iconbitmap("logo.ico")
    root.maxsize(800,800)

    # Add background image
    background_image = tk.PhotoImage(file="background.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = background_image

    # Welcome label (placed on top of background)
    welcome_label = tk.Label(root, 
                           text="Welcome to Salon Management System", 
                           font=("Arial", 16), 
                           bg='#f0f0f0')  # Set background color matching your image
    welcome_label.pack(pady=20)

    # Buttons with transparent background
    button_style = {'bg': '#f0f0f0', 'activebackground': '#e0e0e0'}  # Adjust colors to match your image
    
    if user_role != "customer":
        buttons = [
            ("Services", open_services),
            ("Appointments", lambda: open_appointments(root)),
            ("View Appointments", lambda: view_appointments.create_view_appointments_window(root)),
            ("Billing", open_billing),
            ("View Queries", view_queries),
            ("About Us", open_about)
        ]
    else:
        buttons = [
            ("Services", open_services),
            ("Appointments", lambda: open_appointments(root)),
            ("Contact US", open_contact),
            ("About Us", open_about)
        
        ]

    for text, command in buttons:
        btn = tk.Button(root, 
                        text=text, 
                        command=command,
                        **button_style)
        btn.pack(pady=5)

    # Logout button
    tk.Button(root, 
             text="Logout", 
             command=root.destroy,
             **button_style).pack(pady=10)

# Rest of the functions remain the same
def open_appointments(parent):
    import appointment
    appointment.create_appointment_window(parent)

def open_billing():
    import billing
    billing.create_billing_window()

def open_services():
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
    create_home_window(root, user_role="employee")
    root.mainloop()