import os
import pandas as pd
from pathlib import Path

# Function to load the data with enhanced debugging and path consistency
def load_data(base_path, selected_months, selected_csvs, debug=False):
    # Ensure the base path is normalized
    base_path = Path(base_path)

    # Check if the master folder exists
    if debug:
        print(f"Master folder exists: {base_path}: {'Yes' if base_path.is_dir() else 'No'}")
    if not base_path.is_dir():
        raise FileNotFoundError(f"The master folder does not exist: {base_path}")

    data = {}

    for month in selected_months:
        year, month_number = month.split('_')
        year_folder = f"{year}_V3"
        month_folder = f"{year}_{month_number}"
        month_path = base_path / year_folder / month_folder  # Use Path for consistency

        if debug:
            print(f"Checking directory: {month_path}")

        if month_path.is_dir():  # Ensure it is a directory
            if debug:
                print(f"Directory exists: {month_path}")

            month_data = {}
            for csv_type in selected_csvs:
                if debug:
                    print(f"Processing CSV type: {csv_type}")

                # Construct the file name, handling the special case for LightSpectra
                file_path = None
                if csv_type == "LightSpectra":
                    # Check for both cases with and without space after the dash
                    file_name_with_space = f"{csv_type}- {month_folder}.csv"
                    file_name_without_space = f"{csv_type}-{month_folder}.csv"

                    file_path_with_space = month_path / file_name_with_space
                    file_path_without_space = month_path / file_name_without_space

                    # Determine which file exists
                    if file_path_with_space.exists():
                        file_path = file_path_with_space
                        if debug:
                            print(f"Found file: {file_path}")
                    elif file_path_without_space.exists():
                        file_path = file_path_without_space
                        if debug:
                            print(f"Found file: {file_path}")
                    else:
                        if debug:
                            print(f"LightSpectra file not found for either format in: {month_path}")
                        continue  # Skip if neither file exists

                else:
                    file_name = f"{csv_type}-{month_folder}.csv"
                    file_path = month_path / file_name  # Use Path for consistency
                    if debug:
                        print(f"Checking file: {file_path}")

                if file_path and file_path.exists():
                    if debug:
                        print(f"Loading file: {file_path}")
                    try:
                        # Read the CSV file
                        data_frame = pd.read_csv(file_path, low_memory=False)

                        if debug:
                            print(f"Successfully loaded {len(data_frame)} rows from {file_path}")

                        # Add metadata columns
                        data_frame['Source'] = csv_type
                        data_frame['Year'] = year
                        data_frame['Month'] = month_number

                        # Add to month-level data
                        month_data[csv_type] = data_frame

                    except Exception as e:
                        if debug:
                            print(f"Error loading file {file_path}: {e}")
                        pass
                else:
                    if debug:
                        print(f"File does not exist: {file_path}")

            # Add the month data to the corresponding year
            if year not in data:
                data[year] = {}
            data[year][month] = month_data
        else:
            if debug:
                print(f"Directory does not exist: {month_path}")

    return data
