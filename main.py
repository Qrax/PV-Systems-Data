import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os
import zipfile
import pandas as pd


def process_zip_file(zip_path):
    # Extract the zip file
    extract_path = "extracted_data"
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Prepare to store data
    data = {}

    # Traverse the extracted directories
    for year_folder in os.listdir(extract_path):
        year_path = os.path.join(extract_path, year_folder)
        if os.path.isdir(year_path):  # Ensure it's a directory
            data[year_folder] = {}

            for month_folder in os.listdir(year_path):
                month_path = os.path.join(year_path, month_folder)
                if os.path.isdir(month_path):  # Ensure it's a directory
                    data[year_folder][month_folder] = []

                    for file in os.listdir(month_path):
                        if file.endswith('.csv'):  # Only process CSV files
                            file_path = os.path.join(month_path, file)
                            df = pd.read_csv(file_path)  # Load the CSV into a DataFrame
                            data[year_folder][month_folder].append(df)

    return data

# Example usagea
zip_file_path = "../../../OneDrive - HvA/Jaar_4/PV systems modeling and analysis/Data/wetransfer_solar-field-data_2024-11-18_1414"
data = process_zip_file(zip_file_path)
data
# Accessing data
# For example, access the first CSV of January 2022: data['2022']['01'][0]
