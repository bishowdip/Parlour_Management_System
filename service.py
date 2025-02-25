import tkinter as tk
from tkinter import ttk

# Sample services data
services = [
    {"id": 1, "name": "Haircut", "description": "Professional haircut and styling.", "price": "RS 200"},
    {"id": 2, "name": "Facial", "description": "Rejuvenating facial treatments.", "price": "RS 1000"},
    {"id": 3, "name": "Manicure", "description": "Nail cleaning and polishing.", "price": "RS 1500"},
    {"id": 4, "name": "Pedicure", "description": "Foot care and nail treatment.", "price": "RS 1200"},
    {"id": 5, "name": "Massage", "description": "Relaxing body massage.", "price": "RS 2000"},
    {"id": 6, "name": "Bridal Makeup", "description": "Whole face makeup.", "price": "RS 8000"},
    {"id": 7, "name": "Eyelashes", "description": "Eyelash extensions.", "price": "RS 1500"},
    {"id": 8, "name": "Nail Extension", "description": "Single & both hand.", "price": "RS 1200"},
]

# Create the main application window
root = tk.Tk()
root.title("Parlor Services")
root.iconbitmap("services.ico")

# Create a Treeview widget to display the services
tree = ttk.Treeview(root, columns=("ID", "Name", "Description", "Price"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Description", text="Description")
tree.heading("Price", text="Price")

# Configure column widths (optional)
tree.column("ID", width=50, anchor="center")
tree.column("Name", width=150)
tree.column("Description", width=300)
tree.column("Price", width=100, anchor="center")

tree.pack(fill=tk.BOTH, expand=True)

# Insert services data into the Treeview
for service in services:
    tree.insert("", "end", values=(service["id"], service["name"], service["description"], service["price"]))

# Run the application
root.mainloop()