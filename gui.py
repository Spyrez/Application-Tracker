import tkinter as tk
from tkinter import ttk, messagebox
from db import insert_application, get_all_applications, update_application_in_db

class JobTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Tracker") # Set the title of the window
        self.selected_id = None # Variable to store the ID of the selected application for editing
        self.editing_mode = False # Flag to indicate if the app is in editing mode

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
        # Add Button
        self.add_button = tk.Button(
            root,
            text="Add Application",
            command=self.add_application,
            fg="black",
            bg="#90ee90" # Light green color for the Add button
            )
        self.add_button.grid(row=3, column=1, pady=5) # Add button location in the grid
        # Edit/Save Button
        self.edit_save_button = tk.Button(root,
            text="Edit Selected",
            command=self.toggle_edit_or_save,
            fg="black",
            bg="#87cefa" # Light blue color for the Edit button
        )
        self.edit_save_button.grid(row=3, column=0, pady=5) # Edit button to edit selected application

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
        self.status_combo.current(0) # Reset the status combobox to "Pending"






    # This function is called when the user clicks the "Edit Selected" button
    # It retrieves the selected application from the treeview and populates the entry fields for editing
    def begin_edit_mode(self):
        selected = self.tree.focus()  # Get the currently selected item in the treeview
        if not selected:
            messagebox.showwarning("Selection Error", "Please select an application to edit.")
            return
        
        values = self.tree.item(selected, "values")
        self.selected_id = self.tree.item(selected, "text") # Row ID will be stored in text

        self.company_entry.delete(0, tk.END)  # Clear the company entry field
        self.company_entry.insert(0, values[0])  # Insert the company name into the company entry field

        self.position_entry.delete(0, tk.END)  # Clear the position entry field
        self.position_entry.insert(0, values[1])  # Insert the position into the position entry field

        self.status_var.set(values[2])  # Set the status combobox to the current status of the selected application






    def toggle_edit_or_save(self):
        if not self.editing_mode:
            # START EDITING
            self.begin_edit_mode()

            # Set the editing mode to True and change the button text to "Save Changes"
            self.editing_mode = True
            self.edit_save_button.config(text="Save Changes", bg="#f4c542") # light yellow/orange color for the Save button
            # Disable the Add button while editing
            self.add_button.config(state="disabled", bg="#d3d3d3") # Greyed out color for the Add button
        else:
            # SAVE CHANGES
            self.save_edited_application()

            # Set the editing mode to False and change the button text to "Edit Selected"
            self.editing_mode = False
            self.edit_save_button.config(text="Edit Selected", bg="#87cefa") # Back to Light blue color for the Edit button
            # Re-enable the Add button
            self.add_button.config(state="normal", bg="#90ee90") # Back to Light green color for the Add button






    # This function is called when the user clicks the "Save Changes" button
    # It updates the selected application in the database with the new values
    def save_edited_application(self):
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