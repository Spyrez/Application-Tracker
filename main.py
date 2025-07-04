import os
import tkinter as tk
from db import initialize_database
from gui import JobTrackerApp

# Make sure data/ folder exists
data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(data_folder, exist_ok=True)

# Initialize the database
initialize_database()

# Start the GUI
root = tk.Tk()
app = JobTrackerApp(root)
root.mainloop()