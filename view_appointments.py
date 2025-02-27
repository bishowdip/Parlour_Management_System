import tkinter as tk
from tkinter import ttk, messagebox
from database import get_all_appointments, delete_appointment
from billing import create_billing_window
import tkcalendar



def create_view_appointments_window(parent):
    window = tk.Toplevel(parent)
    window.title("View Appointments")
    window.geometry("1000x600")
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)

    # Search Frame
    search_frame = tk.Frame(window)
    search_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

    # Left side: Search inputs
    input_frame = tk.Frame(search_frame)
    input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Name Search
    name_frame = tk.Frame(input_frame)
    name_frame.pack(side=tk.LEFT, padx=5)
    tk.Label(name_frame, text="Search by Name:").pack(side=tk.LEFT)
    name_search_var = tk.StringVar()
    name_entry = tk.Entry(name_frame, textvariable=name_search_var, width=25)
    name_entry.pack(side=tk.LEFT, padx=5)
    name_entry.bind('<KeyRelease>', lambda e: refresh_appointments())

    # Phone Search
    phone_frame = tk.Frame(input_frame)
    phone_frame.pack(side=tk.LEFT, padx=5)
    tk.Label(phone_frame, text="Search by Phone:").pack(side=tk.LEFT)
    phone_search_var = tk.StringVar()

    # Validation function for phone number input
    def validate_phone_input(action, inserted_text):
        if action == '1':  # Insert action
            return inserted_text.isdigit()
        return True

    # Register validation command
    vcmd = (window.register(validate_phone_input), '%d', '%S')
    def open_billing_from_appointment():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment first!")
            return

        selected_values = tree.item(selected[0], 'values')
        if not selected_values:
            messagebox.showerror("Error", "Could not retrieve appointment details.")
            return

        # Extract appointment details
        appointment_id = selected_values[0]
        customer_name = selected_values[1]
        service_name = selected_values[3]

        # Open billing window as child of the appointments window
        create_billing_window(window, customer_name, service_name)
        
    phone_entry = tk.Entry(
        phone_frame, 
        textvariable=phone_search_var, 
        width=15,
        validate="key",
        validatecommand=vcmd)
    
    phone_entry.pack(side=tk.LEFT, padx=5)
    phone_entry.bind('<KeyRelease>', lambda e: refresh_appointments())

    # Right side: Clear button
    button_frame = tk.Frame(search_frame)
    button_frame.pack(side=tk.RIGHT, padx=5)
    
    def clear_search():
        name_search_var.set('')
        phone_search_var.set('')
        refresh_appointments()
        
    tk.Button(button_frame, text="Clear Search", 
             command=clear_search).pack(side=tk.RIGHT)

    # Treeview Frame
    tree_frame = tk.Frame(window)
    tree_frame.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')

    columns = ("ID", "Name", "Contact", "Service", "Date", "Time", "Status")
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
    
    # Configure columns
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Contact", text="Contact")
    tree.heading("Service", text="Service")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Status", text="Status")

    tree.column("ID", width=50, anchor='center')
    tree.column("Name", width=150)
    tree.column("Contact", width=120)
    tree.column("Service", width=180)
    tree.column("Date", width=100)
    tree.column("Time", width=80)
    tree.column("Status", width=100)

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Bottom Button Frame
    bottom_btn_frame = tk.Frame(window)
    bottom_btn_frame.grid(row=2, column=0, pady=10)

    def refresh_appointments():
        """Refresh appointments with separate filters"""
        tree.delete(*tree.get_children())
        
        name_filter = name_search_var.get().strip().lower()
        phone_filter = phone_search_var.get().strip().lower()

        for appt in get_all_appointments():
            appt_name = appt['customer_name'].lower()
            appt_phone = appt['contact'].lower()
            
            name_match = name_filter in appt_name if name_filter else True
            phone_match = phone_filter in appt_phone if phone_filter else True

            if name_match and phone_match:
                tree.insert('', 'end', values=(
                    appt['id'],
                    appt['customer_name'],
                    appt['contact'],
                    appt['service_name'],
                    appt['appointment_date'],
                    appt['appointment_time'],
                    appt['status']
                ))


    def open_billing_from_appointment():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment first!")
            return

        selected_values = tree.item(selected[0], 'values')
        if not selected_values:
            messagebox.showerror("Error", "Could not retrieve appointment details.")
            return

        # Extract appointment details
        appointment_id = selected_values[0]
        customer_name = selected_values[1]
        service_name = selected_values[3]

        # Open billing window with parent, customer name, and service
        create_billing_window(window, customer_name, service_name)



    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an appointment first!")
            return
            
        appointment_id = tree.item(selected[0], 'values')[0]
        if messagebox.askyesno("Confirm Delete", "Permanently delete this appointment?"):
            delete_appointment(appointment_id)
            refresh_appointments()

    # Bottom buttons
    tk.Button(bottom_btn_frame, text="Generate Bill", 
              command=open_billing_from_appointment).pack(side=tk.LEFT, padx=5)

    tk.Button(bottom_btn_frame, text="Delete Selected", 
             command=delete_selected).pack(side=tk.LEFT, padx=5)
    tk.Button(bottom_btn_frame, text="Refresh List", 
             command=refresh_appointments).pack(side=tk.LEFT, padx=5)
    tk.Button(bottom_btn_frame, text="Close", 
             command=window.destroy).pack(side=tk.LEFT, padx=5)

    refresh_appointments()
    return window

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    appointments_window = create_view_appointments_window(root)
    root.mainloop()