import os
import time
from datetime import timedelta
import shutil  # Import for folder deletion
from tkinter import Tk, Label, Entry, Button, StringVar, ttk

def get_user_input(window):
  """Retrieves user input from GUI elements."""
  deletion_time = float(deletion_time_entry.get())
  folder_name = folder_name_entry.get()
  time_unit = time_unit_var.get().lower()
  return deletion_time, folder_name, time_unit

def create_temp_folder(folder_name):
  """Creates a temporary folder with a random name within the specified folder."""
  random_part = os.urandom(16).hex()[:8]  # Generate random string
  temp_folder_path = os.path.join(folder_name, f"temp_{random_part}")
  os.makedirs(temp_folder_path)  # Create folder using os.makedirs
  return temp_folder_path  # Return the created folder path

def convert_to_seconds(deletion_time, time_unit):
  """Converts the user-provided deletion time to seconds."""
  if time_unit == "seconds":
    return deletion_time
  elif time_unit == "minutes":
    return deletion_time * 60
  elif time_unit == "hours":
    return deletion_time * 3600
  elif time_unit == "days":
    return deletion_time * 86400
  else:
    return None  # Return None for invalid time unit

def delete_folder(temp_folder_path):
  """Deletes the temporary folder and its contents using shutil.rmtree."""
  try:
    shutil.rmtree(temp_folder_path)
    status_label.config(text="Temporary folder deleted successfully.")
  except (FileNotFoundError, PermissionError) as e:
    status_label.config(text=f"Error deleting temporary folder: {e}")

def run_program():
  """Starts the deletion timer based on user input."""
  deletion_time, folder_name, time_unit = get_user_input(window)
  
  # Check if conversion returned a valid value (could be None if invalid input)
  if deletion_time is not None:
    seconds_to_wait = convert_to_seconds(deletion_time, time_unit)
    temp_folder_path = create_temp_folder(folder_name)  # Call function only if conversion successful
    
    status_label.config(text=f"Folder will be deleted in approximately {deletion_time} {time_unit}.")
    print(temp_folder_path)
    window.after(int(seconds_to_wait * 1000), delete_folder, folder_name)  # Schedule deletion after delay

window = Tk()
window.title("TFC")

# Labels
deletion_time_label = Label(window, text="Deletion Time:")
deletion_time_label.grid(row=0, column=0)

Name = Label(window, text="Name:    ")
Name.grid(row=2, column=0)

time_unit_label = Label(window, text="Time Unit:")
time_unit_label.grid(row=1, column=0)

status_label = Label(window, text="")
status_label.grid(row=4, columnspan=2)

# Entries
deletion_time_entry = Entry(window)
deletion_time_entry.grid(row=0, column=1)

folder_name_entry = Entry(window)
folder_name_entry.grid(row=2, columnspan=2)

# Time Unit Selection (Dropdown)
time_unit_var = StringVar(window)
time_unit_var.set("seconds")  # Default selection

time_unit_dropdown = ttk.Combobox(window, textvariable=time_unit_var, values=("seconds", "minutes", "hours", "days"))
time_unit_dropdown.grid(row=1, column=1)

# Button
run_button = Button(window, text="Create Folder", command=run_program)
run_button.grid(row=3, columnspan=2)

# Allow closing the window
window.protocol("WM_DELETE_WINDOW", window.destroy)

window.mainloop()