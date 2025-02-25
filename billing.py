import tkinter as tk
from tkinter import messagebox
from database import get_services, create_transaction

def create_billing_window(parent=None, customer_name="", preselected_service=""):
    # Create a hidden root window if running standalone
    if parent is None:
        root = tk.Tk()
        root.withdraw()
        billing_window = tk.Toplevel(root)
        billing_window.protocol("WM_DELETE_WINDOW", root.destroy)  # Close entire app
    else:
        billing_window = tk.Toplevel(parent)

    billing_window.title("Billing")
    billing_window.geometry("500x600")

    # Fetch services
    services = get_services()
    prices = {service[1]: service[2] for service in services}
    quantities = {service[1]: 0 for service in services}
    quantity_labels = {}

    # Customer Name Label
    tk.Label(
        billing_window,
        text=f"Customer: {customer_name}",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    # Helper functions
    def adjust_quantity(service, delta):
        quantities[service] += delta
        if quantities[service] < 0:
            quantities[service] = 0
        quantity_labels[service].config(text=str(quantities[service]))
        update_total()

    def update_total():
        total = sum(qty * prices[srv] for srv, qty in quantities.items())
        total_label.config(text=f"Total: NPR {total}")

    def calculate_total():
        total = sum(qty * prices[srv] for srv, qty in quantities.items() if qty > 0)
        services_used = [f"{srv} x{qty}" for srv, qty in quantities.items() if qty > 0]
        create_transaction(customer_name, total, ", ".join(services_used))
        messagebox.showinfo("Success", "Transaction saved!")
        billing_window.destroy()
        if parent is None:
            root.destroy()  # Close hidden root

    # Add services to UI
    for service in services:
        service_name = service[1]
        frame = tk.Frame(billing_window)
        frame.pack(pady=5)

        tk.Label(frame, text=f"{service_name} (NPR {prices[service_name]})").pack(side=tk.LEFT)
        quantity_label = tk.Label(frame, text="0")
        quantity_label.pack(side=tk.LEFT, padx=10)
        quantity_labels[service_name] = quantity_label

        # Preselect service if provided
        if service_name == preselected_service:
            quantities[service_name] = 1
            quantity_label.config(text="1")

        # Buttons
        tk.Button(frame, text="-", command=lambda s=service_name: adjust_quantity(s, -1)).pack(side=tk.LEFT)
        tk.Button(frame, text="+", command=lambda s=service_name: adjust_quantity(s, 1)).pack(side=tk.LEFT)

    # Total label and button
    total_label = tk.Label(billing_window, text="Total: NPR 0", font=("Arial", 14))
    total_label.pack(pady=20)
    tk.Button(billing_window, text="Calculate Total", command=calculate_total).pack(pady=10)

    # Start mainloop if standalone
    if parent is None:
        root.mainloop()

if __name__ == "__main__":
    create_billing_window()  # Standalone mode