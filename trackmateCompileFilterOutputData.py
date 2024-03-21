'''
 Compiles and filters different data metrics from TrackMate's tracks output file

 Assumes all output files are in different folders within one main directory

 Processes one condition and one replicate
 '''

import os
import pandas as pd
import numpy as np
from tkinter import filedialog
import tkinter as tk

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Ask user to select the input directory using a file dialog
input_directory = filedialog.askdirectory(title="Select Input Directory")

# Check if a directory was selected
if not input_directory:
    print("No directory selected. Exiting...")
    exit()

# Ask the user for track duration to filter out
track_duration_input = int(input("Enter the minimum track duration (sec) you would like (Please enter whole number): "))

column_titles = ['TRACK_INDEX', 'TRACK_ID', 'NUMBER_SPOTS', 'NUMBER_GAPS', 'NUMBER_SPLITS', 'NUMBER_MERGES',
                 'NUMBER_COMPLEX', 'LONGEST_GAP', 'TRACK_START', 'TRACK_STOP', 'TRACK_DISPLACEMENT',
                 'TRACK_X_LOCATION', 'TRACK_Y_LOCATION', 'TRACK_Z_LOCATION', 'TRACK_MEAN_SPEED', 'TRACK_MAX_SPEED',
                 'TRACK_MIN_SPEED', 'TRACK_MEDIAN_SPEED', 'TRACK_STD_SPEED', 'TRACK_MEAN_QUALITY',
                 'TOTAL_DISTANCE_TRAVELED', 'MAX_DISTANCE_TRAVELED', 'CONFINEMENT_RATIO', 'MEAN_STRAIGHT_LINE_SPEED',
                 'LINEARITY_OF_FORWARD_PROGRESSION', 'MEAN_DIRECTIONAL_CHANGE_RATE']

while True:
    # Ask the user for which data they would like to extract
    column_input = input("Enter the exact column name of the data you would like to extract (EX. TRACK_MEAN_SPEED): ")
    if column_input in column_titles:
        break
    else:
        print("Invalid entry, please enter a column title exactly as written in column_titles.")



# Create a list to store NumPy arrays
result_arrays = []

# Iterate over folders in the directory
for folder_name in os.listdir(input_directory):
    folder_path = os.path.join(input_directory, folder_name)
    
    # Check if the item in the directory is a folder
    if os.path.isdir(folder_path):
        print('file exists')
        # Check if export.csv exists in the folder
        export_csv_path = os.path.join(folder_path, 'export.csv')
        if not os.path.exists(export_csv_path):
            print(f"export.csv not found in folder '{folder_name}'. Skipping...")
            continue
        
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(export_csv_path)

        # Convert column_input and 'TRACK_DURATION' to numeric values
        df[column_input] = pd.to_numeric(df[column_input], errors='coerce')
        df['TRACK_DURATION'] = pd.to_numeric(df['TRACK_DURATION'], errors='coerce')

        # Filter rows starting from the 5th row based on conditions
        filtered_rows = df.iloc[4:].loc[(~df[column_input].isna()) & (df['TRACK_DURATION'] >= track_duration_input)]

        # Extract values from column_input and convert them to a NumPy array
        result_array = np.array(filtered_rows[column_input])

        # Add the NumPy array to the list
        result_arrays.append(result_array)

if result_arrays:
    # Create a DataFrame from the list of arrays
    result_df = pd.DataFrame(result_arrays).T
    result_df.columns = [f'Column_{i+1}' for i in range(result_df.shape[1])]

    # Save the resulting DataFrame to a CSV file
    result_df.to_csv(os.path.join(input_directory, column_input+str(track_duration_input)+ 'sec'+'.csv'), index=False)
    print("Results saved successfully.")
else:
    print("No valid data found to save.")