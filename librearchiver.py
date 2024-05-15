#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog
import subprocess
import threading

def run_7za(command):
    try:
        # Print the command being executed
        print("Executing command:", " ".join(command))
        
        # Convert the command list to a string
        command_str = " ".join(command)
        
        # Run the command
        process = subprocess.Popen(command_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        
        # Capture output and error streams
        stdout, stderr = process.communicate()
        
        # Display the output
        root.after(0, update_output, stdout)
        
        # Display any errors
        if stderr:
            root.after(0, update_output, "\nError:\n" + stderr)
    except Exception as e:
        # If there's an error, display it
        root.after(0, update_output, "Error: " + str(e) + "\nCommand: " + command_str)

def update_output(text):
    # Clear previous content
    output_text.delete("1.0", tk.END)
    # Display new content
    output_text.insert(tk.END, text)

def add_files_to_archive():
    # Get the selected file(s)
    file_paths = filedialog.askopenfilenames()
    if not file_paths:
        return
    
    # Ask user for archive name
    archive_name = filedialog.asksaveasfilename(filetypes=[("7z files", "*.7z")], defaultextension=".7z")
    if not archive_name:
        return
    
    # Get the compression level from the scale
    compression_level = compression_scale.get()
    
    # Construct the command
    command = ["7za", "a", "-t7z", "-mx" + str(compression_level), archive_name]
    command.extend(file_paths)
    
    # Run the command in a separate thread
    threading.Thread(target=lambda: run_7za(command)).start()

# Create the tkinter window
root = tk.Tk()
root.title("LibreArchiver")

# Create a button to add files to archive
add_button = tk.Button(root, text="Add Files to Archive", command=add_files_to_archive)
add_button.pack(pady=5)

# Create a text widget to display the output
output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=5)

# Create a scale for compression level
compression_scale = tk.Scale(root, from_=0, to=9, orient=tk.HORIZONTAL, length=400, label="Compression Level")
compression_scale.set(5)  # Set default value to 5
compression_scale.pack(pady=5)


# Run the tkinter main loop
root.mainloop()
