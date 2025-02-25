# about.py
import tkinter as tk

def create_about_window():
    # Create the main window
    root = tk.Tk()
    root.title("About Us")
    root.geometry("600x500")

    # Add a header label
    header_label = tk.Label(root, text="About Us", font=("Arial", 24, "bold"))
    header_label.pack(pady=20)

    # Company Mission Section
    mission_label = tk.Label(root, text="Our Mission", font=("Arial", 18, "underline"))
    mission_label.pack(pady=10)
    mission_text = tk.Label(root, text="At our company, we strive to deliver the best services and products to our customers. We focus on quality, innovation, and customer satisfaction.", wraplength=500, justify="left")
    mission_text.pack(pady=10)

    # Company Values Section
    values_label = tk.Label(root, text="Our Values", font=("Arial", 18, "underline"))
    values_label.pack(pady=10)
    values_text = tk.Label(root, text="Integrity, Excellence, Innovation, and Teamwork are the core values that guide our business operations and relationships with clients.", wraplength=500, justify="left")
    values_text.pack(pady=10)

    # Contact Information Section
    contact_label = tk.Label(root, text="Contact Information", font=("Arial", 18, "underline"))
    contact_label.pack(pady=10)
    contact_info = tk.Label(root, text="Email: beautybliss@gmail.com\nPhone: +9779876543210\nAddress: Maitidevi,Kathmandu", wraplength=500, justify="left")
    contact_info.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_about_window()