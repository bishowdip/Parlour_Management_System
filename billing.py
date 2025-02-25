# billing.py
import tkinter as tk
from tkinter import messagebox
from database import get_services, create_transaction

def calculate_total():
    total = 0
    services_used = []
    for service, quantity in quantities.items():
        if quantity > 0:
            total += quantity * prices[service]
            services_used.append(f"{service} x{quantity}")
    total_label.config(text=f"Total: NPR {total}")
    create_transaction("Customer Name", total, ", ".join(services_used))
    messagebox.showinfo("Success", "Transaction saved successfully!")

def adjust_quantity(service, delta):
    quantities[service] += delta
    if quantities[service] < 0:
        quantities[service] = 0
    quantity_labels[service].config(text=str(quantities[service]))

def create_billing_window():
    global quantities, quantity_labels, total_label, prices

    # Get services and initialize quantities
    services = get_services()
    prices = {service[1]: service[2] for service in services}
    quantities = {service[1]: 0 for service in services}
    quantity_labels = {}

    # Create the main window
    root = tk.Tk()
    root.title("Billing")
    root.geometry("500x600")
    root.iconbitmap("billing.ico")

    # Add services with quantity adjustment buttons
    for service in services:
        service_frame = tk.Frame(root)
        service_frame.pack(pady=5)

        # Service name and price
        tk.Label(service_frame, text=f"{service[1]} (NPR {service[2]}):").pack(side=tk.LEFT)

        # Quantity label
        quantity_label = tk.Label(service_frame, text="0")
        quantity_label.pack(side=tk.LEFT, padx=10)
        quantity_labels[service[1]] = quantity_label

        # Decrease button
        tk.Button(service_frame, text="-", command=lambda s=service[1]: adjust_quantity(s, -1)).pack(side=tk.LEFT)

        # Increase button
        tk.Button(service_frame, text="+", command=lambda s=service[1]: adjust_quantity(s, 1)).pack(side=tk.LEFT)

    # Total label
    total_label = tk.Label(root, text="Total: NPR 0", font=("Arial", 14))
    total_label.pack(pady=20)

    # Calculate Total Button
    tk.Button(root, text="Calculate Total", command=calculate_total).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_billing_window()