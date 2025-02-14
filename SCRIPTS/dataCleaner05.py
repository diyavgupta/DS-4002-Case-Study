import csv
import pandas as pd
import os

# Define input and output files
input_files = ["DATA/cleaned_final_statements.csv", "DATA/Clean_Inmate_Info.csv"]
output_file = "combined_fs_ii.csv"

def load_csv(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"Skipping {file_path}, file not found.")
        return None

# Load the datasets
df_statements = load_csv("DATA/cleaned_final_statements.csv")
df_inmate_info = load_csv("DATA/Clean_Inmate_Info.csv")

if df_statements is not None and df_inmate_info is not None:
    # Standardize column names for easier matching
    df_statements.rename(columns={'Inmate Name': 'Name'}, inplace=True)
    df_statements['Name'] = df_statements['Name'].astype(str).str.strip().str.lower()
    df_inmate_info['Name'] = df_inmate_info['Name'].astype(str).str.strip().str.lower()
    
    # Extract last names for matching
    df_inmate_info['Last Name'] = df_inmate_info['Name'].apply(lambda x: x.split(',')[0].strip().lower() if isinstance(x, str) and ',' in x else x)
    
    # Merge on last names only to align execution numbers correctly
    merged_df = df_statements.merge(df_inmate_info, left_on='Name', right_on='Last Name', how='outer', indicator=True)
    
    # Selecting required columns for the output CSV
    output_columns = [
        'Name', 'Execution Number', 'Last Statement',
        'Date Received', 'Education Level', 'Date of Offense', 
        'Prior Occupation', 'Prior Prison Record', 'Summary of Incident'
    ]
    
    # Keeping only the necessary columns and formatting for separation
    final_df = merged_df[output_columns]
    
    # Save the corrected data
    final_df.to_csv(output_file, index=False, sep="|")  # Using | for clear separation
    
    print(f"Combined CSV saved as {output_file}")
else:
    print("Error loading files, unable to proceed with combining.")