import tkinter as tk
from tkinter import ttk, messagebox
from database import get_services, add_service, delete_service

def create_service_window(role):
    """Create and display the services window."""
    # Create a Toplevel window
    service_window = tk.Toplevel()
    service_window.title("Parlor Services")
    service_window.geometry("800x500")
    service_window.iconbitmap("services.ico")

    # Create a Treeview widget to display the services
    tree = ttk.Treeview(service_window, columns=("ID", "Name", "Price", "Description"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Price", text="Price")
    tree.heading("Description", text="Description")

    # Configure column widths
    tree.column("ID", width=50, anchor="center")
    tree.column("Name", width=150)
    tree.column("Price", width=100, anchor="center")
    tree.column("Description", width=300)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Refresh the Treeview with services from the database
    def refresh_services():
        tree.delete(*tree.get_children())  # Clear existing data
        for service in get_services():
            # Ensure the order matches: ID, Name, Price, Description
            tree.insert("", "end", values=(service[0], service[1], f"RS {service[2]}", service[3]))

    # Add a new service
    def add_new_service():
        add_window = tk.Toplevel(service_window)
        add_window.title("Add New Service")
        add_window.geometry("400x300")

        # Labels and Entry fields
        tk.Label(add_window, text="Service Name:").grid(row=0, column=0, padx=10, pady=10)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Price:").grid(row=1, column=0, padx=10, pady=10)
        price_entry = tk.Entry(add_window)
        price_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Description:").grid(row=2, column=0, padx=10, pady=10)
        description_entry = tk.Entry(add_window)
        description_entry.grid(row=2, column=1, padx=10, pady=10)

        # Save button
        def save_service():
            name = name_entry.get().strip()
            price = price_entry.get().strip()
            description = description_entry.get().strip()

            if not name or not price or not description:
                messagebox.showwarning("Error", "All fields are required!")
                return

            try:
                price = float(price)  # Convert price to float
                add_service(name, price, description)  # Add to database
                messagebox.showinfo("Success", "Service added successfully!")
                refresh_services()  # Refresh the Treeview
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Price must be a number!")

        tk.Button(add_window, text="Save", command=save_service).grid(row=3, column=0, columnspan=2, pady=10)

    # Delete selected service
    def delete_selected_service():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a service to delete!")
            return

        service_id = tree.item(selected[0], "values")[0]  # Get ID of selected service
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this service?"):
            delete_service(service_id)  # Delete from database
            refresh_services()  # Refresh the Treeview

    # Button frame
    button_frame = tk.Frame(service_window)
    button_frame.pack(pady=10)

    # Add and Delete buttons (only for employees)
    if role == "employee":
        tk.Button(button_frame, text="Add Service", command=add_new_service).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Selected", command=delete_selected_service).pack(side=tk.LEFT, padx=5)

    # Refresh services on window load
    refresh_services()

    # Run the Toplevel window
    service_window.mainloop()

# For testing purposes
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Simulate a logged-in user with a role
    logged_in_role = "employee"  # Change this to "customer" to test customer access
    create_service_window(logged_in_role)
    root.mainloop()