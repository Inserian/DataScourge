import os
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class SpaceFinderGUI:
    def __init__(self, master):
        self.master = master
        master.title("SpaceFinder")

        # Create directory selection label and button
        self.dir_label = ttk.Label(master, text="Select directory to scan:")
        self.dir_label.grid(row=0, column=0, sticky="W")
        self.dir_button = ttk.Button(master, text="Browse", command=self.select_directory)
        self.dir_button.grid(row=0, column=1, padx=5, pady=5, sticky="E")
        self.dir_entry = ttk.Entry(master)
        self.dir_entry.grid(row=0, column=2, padx=5, pady=5, sticky="WE")
        self.dir_entry.insert(tk.END, os.getcwd())

        # Create file size entry and label
        self.file_size_label = ttk.Label(master, text="Minimum file size (MB):")
        self.file_size_label.grid(row=1, column=0, sticky="W")
        self.file_size_entry = ttk.Entry(master)
        self.file_size_entry.grid(row=1, column=1, padx=5, pady=5, sticky="E")
        self.file_size_entry.insert(tk.END, "100")

        # Create months unused entry and label
        self.months_unused_label = ttk.Label(master, text="Months unused:")
        self.months_unused_label.grid(row=2, column=0, sticky="W")
        self.months_unused_entry = ttk.Entry(master)
        self.months_unused_entry.grid(row=2, column=1, padx=5, pady=5, sticky="E")
        self.months_unused_entry.insert(tk.END, "6")

        # Create exclude extensions entry and label
        self.exclude_extensions_label = ttk.Label(master, text="Exclude files with extensions:")
        self.exclude_extensions_label.grid(row=3, column=0, sticky="W")
        self.exclude_extensions_entry = ttk.Entry(master)
        self.exclude_extensions_entry.grid(row=3, column=1, padx=5, pady=5, sticky="E")
        self.exclude_extensions_entry.insert(tk.END, ".jpg,.png,.pdf")

        # Create exclude names entry and label
        self.exclude_names_label = ttk.Label(master, text="Exclude files with names:")
        self.exclude_names_label.grid(row=4, column=0, sticky="W")
        self.exclude_names_entry = ttk.Entry(master)
        self.exclude_names_entry.grid(row=4, column=1, padx=5, pady=5, sticky="E")
        self.exclude_names_entry.insert(tk.END, "backup,old")

        # Create scan button
        self.scan_button = ttk.Button(master, text="Scan", command=self.scan_directory)
        self.scan_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        # Create result label
        self.result_label = ttk.Label(master, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

    def select_directory(self):
        # Open file dialog to select directory
        directory = filedialog.askdirectory()
        # If directory is selected, update directory entry
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(tk.END, directory)

    def scan_directory(self):
        # Get directory and parameters from GUI
        directory = self.dir_entry.get()
        min_file_size = int(self.file_size_entry.get()) * 1024 * 1024
        months_unused = int(self.months_unused_entry.get())
        exclude_extensions = self.exclude_extensions_entry.get().split(',')
        exclude_names = self.exclude_names_entry.get().split(',')

        # Initialize an empty list to store results
        results = []

        # Iterate over all files and folders in the directory and its subdirectories
        for root, dirs, files in os.walk(directory):
            for name in files:
                filepath = os.path.join(root, name)
                # Exclude files by extension and name
                if any(filepath.endswith(ext) for ext in exclude_extensions):
                    continue
                if any(name.lower().startswith(exclude_name) for exclude_name in exclude_names):
                    continue
                try:
                    # Get file size
                    size = os.path.getsize(filepath)
                except FileNotFoundError:
                    # Skip this file and continue with the next one
                    continue

                # Get date last accessed
                accessed_time = os.path.getatime(filepath)
                accessed_date = datetime.datetime.fromtimestamp(accessed_time)
                # Calculate how many months ago the file was last accessed
                months_since_accessed = (datetime.datetime.now() - accessed_date).days // 30
                # Check if file is larger than minimum size and has not been accessed in several months
                if size > min_file_size and months_since_accessed >= months_unused:
                    # Add file to results list
                    results.append({'Name': name, 'Path': filepath, 'Size': size, 'Last Accessed': accessed_date})

        # Update result label with report
        if len(results) == 0:
            self.result_label.configure(text="No large and unused files were found.")
        else:
            report = "Large and unused files:\n\n"
            for result in results:
                report += f"{result['Path']} ({result['Size'] / (1024 * 1024):.2f} MB) last accessed on {result['Last Accessed'].strftime('%m/%d/%Y')} at {result['Last Accessed'].strftime('%I:%M %p')}\n"
            report += f"\nFound {len(results)} large and unused files."
            self.result_label.configure(text=report)

root = tk.Tk()
my_gui = SpaceFinderGUI(root)
root.mainloop()
