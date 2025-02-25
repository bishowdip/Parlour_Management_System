import tkinter as tk
from tkinter import ttk

# Sample services data
services = [
    {"id": 1, "name": "Haircut", "description": "Professional haircut and styling."},
    {"id": 2, "name": "Facial", "description": "Rejuvenating facial treatments." },
    {"id": 3, "name": "Manicure", "description": "Nail cleaning and polishing."},
    {"id": 4, "name": "Pedicure", "description": "Foot care and nail treatment."},
    {"id": 5, "name": "Massage", "description": "Relaxing body massage."},
    {"id":6, "name": "Bridal Makeup", "description": "Whole face makeup."},
    {"id":6, "name": "Eyelashes", "description": "Whole face makeup."},
    {"id":6, "name": "Nail Extensiom", "description": "single & both hand."},
]

# Create the main application window
root = tk.Tk()
root.title("Parlor Services")
root.iconbitmap("services.ico")
# Create a Treeview widget to display the services
tree = ttk.Treeview(root, columns=("ID", "Name", "Description"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Description", text="Description")


tree.pack(fill=tk.BOTH, expand=True)

# Insert services data into the Treeview
for service in services:
    tree.insert("", "end", values=(service["id"], service["name"], service["description"]))

# Run the application
root.mainloop()
