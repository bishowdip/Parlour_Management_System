import tkinter as tk
from tkinter import ttk, messagebox
from database import get_all_contact_queries, update_query_status

def update_status(query_id):
    if messagebox.askyesno("Confirm", "Mark this query as resolved?"):
        update_query_status(query_id, "Resolved")
        refresh_queries()

def refresh_queries():
    # Clear existing data in the Treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Fetch queries from the database
    queries = get_all_contact_queries()
    
    # Debugging: Print the structure of the first query
    if queries:
        print("First query structure:", queries[0])
    
    # Insert queries into the Treeview
    for query in queries:
        # Use get() method to provide a default value if 'status' is missing
        status = query['status'] if 'status' in query.keys() else 'Pending'  # Correct
            # Default to 'Pending' if status is missing
        tree.insert("", tk.END, values=(
            query['id'],
            query['name'],
            query['email'],
            query['subject'],
            query['message'],
            query['submitted_at'],
            status  # Use the status value, defaulting to 'Pending' if missing
        ))
def view_queries():
    global tree  # Make tree global for refresh_queries to access
    
    # Create a new window to display queries
    query_window = tk.Toplevel()
    query_window.title("Customer Queries")
    query_window.geometry("800x500")

    # Create Treeview with columns
    tree = ttk.Treeview(query_window, 
                      columns=("ID", "Name", "Email", "Subject", "Message", "Submitted At", "Status"), 
                      show="headings")
    
    # Configure columns
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Subject", text="Subject")
    tree.heading("Message", text="Message")
    tree.heading("Submitted At", text="Submitted At")
    tree.heading("Status", text="Status")
    
    tree.column("ID", width=50, anchor='center')
    tree.column("Status", width=100, anchor='center')
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(query_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    # Pack components
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Add status update button
    btn_frame = tk.Frame(query_window)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="Mark as Resolved", 
             command=lambda: update_selected_status()).pack(side=tk.LEFT, padx=5)
    
    tk.Button(btn_frame, text="Refresh", 
             command=refresh_queries).pack(side=tk.LEFT, padx=5)


    
    def update_status(query_id):
        if messagebox.askyesno("Confirm", "Mark this query as resolved?"):
            update_query_status(query_id, "Resolved")
            refresh_queries()  # Refresh the UI after updating
    def update_selected_status():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a query!")
            return
        
        query_id = tree.item(selected[0])['values'][0]  # Get ID of selected query
        update_status(query_id)  # Call update_status with the correct ID


    # Load initial data
    refresh_queries()
    query_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    view_queries()
    root.mainloop()