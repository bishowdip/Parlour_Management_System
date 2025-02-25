import tkinter as tk
from tkinter import ttk, messagebox
from database import get_all_contact_queries

def view_queries():
    """Function to display all submitted queries in a new window."""
    queries = get_all_contact_queries()  # Fetch queries from the database

    # Create a new window to display queries
    query_window = tk.Toplevel()
    query_window.title("View Queries")
    query_window.geometry("600x400")

    # Use a Treeview widget to display the queries in a table-like format
    tree = ttk.Treeview(query_window, columns=("ID", "Name", "Email", "Subject", "Message", "Submitted At"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Subject", text="Subject")
    tree.heading("Message", text="Message")
    tree.heading("Submitted At", text="Submitted At")
    tree.pack(fill=tk.BOTH, expand=True)

    # Insert queries into the Treeview
    for query in queries:
        tree.insert("", tk.END, values=query)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(query_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)