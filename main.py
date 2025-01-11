import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


# Function to process selected months and CSV files
def process_selected_data(selected_months, selected_csvs, base_path):
    data = {}

    for month in selected_months:
        year, month_number = month.split('_')
        year_folder = f"{year}_V3"
        month_folder = f"{year}_{month_number}"
        month_path = os.path.join(base_path, year_folder, month_folder)

        if os.path.isdir(month_path):  # Ensure it is a directory
            month_data = {}
            for csv_type in selected_csvs:
                # Define the file path
                file_name = f"{csv_type}-{month_folder}.csv"
                file_path = os.path.join(month_path, file_name)

                try:
                    # Read the CSV file
                    data_frame = pd.read_csv(file_path, low_memory=False)

                    # Add metadata columns
                    data_frame['Source'] = csv_type
                    data_frame['Year'] = year
                    data_frame['Month'] = month_number

                    # Add to month-level data
                    month_data[csv_type] = data_frame

                except FileNotFoundError:
                    print(f"File not found: {file_name} in {month_folder}")

            # Add the month data to the corresponding year
            if year not in data:
                data[year] = {}
            data[year][month] = month_data

    return data


# GUI for selecting months and CSV files
def selection_gui(base_path):
    def on_submit():
        selected_months = [month for month, var in month_checkboxes.items() if var.get()]
        selected_csvs = [csv for csv, var in csv_checkboxes.items() if var.get()]

        if not selected_months:
            messagebox.showwarning("No Selection", "Please select at least one month.")
            return
        if not selected_csvs:
            messagebox.showwarning("No Selection", "Please select at least one CSV file type.")
            return

        root.destroy()

        # Process data and create the hierarchical structure
        final_data = process_selected_data(selected_months, selected_csvs, base_path)

        # Display a preview of the processed structure in the terminal
        print("\nData Structure Overview:")
        for year, months in final_data.items():
            print(f"Year: {year}")
            for month, month_data in months.items():
                print(f"  Month: {month}")
                for csv_type, df in month_data.items():
                    print(f"    {csv_type}: {len(df)} rows")

    # Create the main GUI window
    root = tk.Tk()
    root.title("Select Months and CSV Files")
    root.geometry("1200x800")  # Set window size to maximize available screen space

    # Title label
    tk.Label(root, text="Select the months and CSV files you want to process:", font=("Arial", 16, "bold")).pack(pady=10)

    # Section for month selection
    month_frame = ttk.LabelFrame(root, text="Months", padding=(10, 10))
    month_frame.pack(fill="both", expand=True, padx=10, pady=5)

    month_checkboxes = {}
    row, col = 0, 0
    for year_folder in os.listdir(base_path):
        year_path = os.path.join(base_path, year_folder)
        if os.path.isdir(year_path):
            for month_folder in os.listdir(year_path):
                month_path = os.path.join(year_path, month_folder)
                if os.path.isdir(month_path):
                    var = tk.BooleanVar()
                    month_checkboxes[month_folder] = var
                    cb = tk.Checkbutton(month_frame, text=month_folder, variable=var, font=("Arial", 12))
                    cb.grid(row=row, column=col, sticky="w", padx=10, pady=5)
                    col += 1
                    if col >= 6:  # Change number of columns here to adjust layout
                        col = 0
                        row += 1

    # Section for CSV file selection
    csv_frame = ttk.LabelFrame(root, text="CSV Files", padding=(10, 10))
    csv_frame.pack(fill="both", expand=True, padx=10, pady=5)

    csv_checkboxes = {}
    csv_types = ["IVCurves", "LightSpectra", "SolarFieldData"]
    row = 0
    for csv_type in csv_types:
        var = tk.BooleanVar()
        csv_checkboxes[csv_type] = var
        cb = tk.Checkbutton(csv_frame, text=csv_type, variable=var, font=("Arial", 12))
        cb.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        row += 1

    # Submit button
    tk.Button(root, text="Submit", command=on_submit, font=("Arial", 14), bg="green", fg="white").pack(pady=20)

    root.mainloop()


# Base file path
base_path = "../../OneDrive - HvA/Jaar_4/PV systems modeling and analysis/Data/data_folder"

# Run the selection GUI
selection_gui(base_path)
