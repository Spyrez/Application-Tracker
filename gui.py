import tkinter as tk
from tkinter import ttk, messagebox
from db import insert_application, get_all_applications, update_application_in_db

class JobTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Tracker") # Set the title of the window
        self.selected_id = None # Variable to store the ID of the selected application for editing

        # Company Label and Entry
        tk.Label(root, text="Company Name").grid(row=0, column=0)
        self.company_entry = tk.Entry(root)
        self.company_entry.grid(row=0, column=1)
       
        # Position Label and Entry
        tk.Label(root, text="Job Position").grid(row=1, column=0)
        self.position_entry = tk.Entry(root)
        self.position_entry.grid(row=1, column=1)

        # Status Label and Combobox drop down menu
        # Combobox for selecting status from "Pending/Rejected" with default value "Pending"
        tk.Label(root, text="Status").grid(row=2, column=0)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(root, textvariable=self.status_var, values=["Pending", "Rejected"])
        self.status_combo.current(0)
        self.status_combo.grid(row=2, column=1)

        # BUTTONS
        tk.Button(root, text="Add Application", command=self.add_application).grid(row=3, column=0, pady=5) # Add button to add application to the database
        tk.Button(root, text="Edit Selected", command=self.load_selected_for_edit).grid(row=3, column=1, pady=5) # Edit button to edit selected application
        tk.Button(root, text="Update Application", command=self.update_application).grid(row=5, columnspan=2, pady=10) # Update button to update application in the database



        # Treeview table to display applications
        # It has three columns: Company, Position, and Status
        self.tree = ttk.Treeview(root, columns=("Company", "Position", "Status"), show="headings")
        # Loop to create the headings and set column widths of the treeview
        for col in ("Company", "Position", "Status"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=4, columnspan=2, pady=10) # columnspan=2 to span both columns(center) and pady for vertical spacing
        
        # Displays the applications in the treeview when opening the app
        # Calls the refresh_applications method to populate the treeview with data from the database
        self.refresh_applications()






    def add_application(self):
        # Get input values
        # Strip whitespace from company and position entries
        company = self.company_entry.get().strip()
        position = self.position_entry.get().strip()
        status = self.status_var.get()

        # Check if both company and position are provided
        # If either is empty, show an error message
        if not company or not position:
            messagebox.showerror("Input Error", "Please enter BOTH company and position.")
            return

        # Calls function from 'db.py' to insert the application into the database
        # It passes the company, position, and status
        insert_application(company, position, status)
        # After inserting, it refreshes the treeview to show the latest applications
        self.refresh_applications()
        self.company_entry.delete(0, tk.END) # Clear the company entry field
        self.position_entry.delete(0, tk.END) # Clear the position entry field
        self.status_var.set("Pending") # Reset the status combobox to "Pending"





    def load_selected_for_edit(self):
        selected = self.tree.focus()  # Get the currently selected item in the treeview
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an application to edit.")
            return
        
        values = self.tree.item(selected, "values")
        self.selected_id = self.tree.item(selected, "text") # Row ID will be stored in text

        self.company_entry.delete(0, tk.END)  # Clear the company entry field
        self.company_entry.insert(0, values[0])  # Insert the company name into

        self.position_entry.delete(0, tk.END)  # Clear the position entry field
        self.position_entry.insert(0, values[1])  # Insert the position into the position entry field

        self.status_var.set(values[2])  # Set the status combobox to the current status of the selected application




    def update_application(self):
        if self.selected_id is None:
            messagebox.showwarning("Selection Error", "Please select an application to update.")
            return
        
        company = self.company_entry.get().strip()
        position = self.position_entry.get().strip()
        status = self.status_var.get()

        if not company or not position:
            messagebox.showerror("Input Error", "Please enter BOTH company and position.")
            return
        
        update_application_in_db(int(self.selected_id), company, position, status)
        self.selected_id = None
        self.refresh_applications()

        self.company_entry.delete(0, tk.END) # Clear the company entry field
        self.position_entry.delete(0, tk.END) # Clear the position entry field
        self.status_combo.current(0)  # Reset the status combobox to "Pending"






    # Refresh the treeview to show the latest applications
    def refresh_applications(self):
        # Clear the treeview before inserting new data
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Fetch all applications from the database and insert them into the treeview
        # Calls function from 'db.py' to get all applications
        # This function returns a list of tuples containing the company, position, and status
        # It then inserts each application into the treeview
        for app in get_all_applications():
            app_id, company, position, status = app
            self.tree.insert("", tk.END, text=str(app_id), values=(company, position, status))