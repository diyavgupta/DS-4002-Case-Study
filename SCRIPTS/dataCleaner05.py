## dataCleaner05.py Script
## Required packages: pandas
## Params: file1 (deathRowInital.csv), file2 (Clean_Inmate_Info.csv), file3 (cleaned_final_statements.csv), output_file (Combined.csv)
## Function: Uses pandas to create seperate data frames for each csv file which only inlcudes the target rows, the data frames are then combined using the execution number as the identifying vairable for each Inmate across the different CSV files. The complete entries are stored at the top of the new Combined_Data.csv file, and the incomplete ones are stored below.

import pandas as pd

def combine_csv_files(file1, file2, file3, output_file):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    df3 = pd.read_csv(file3)

    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()
    df3.columns = df3.columns.str.strip()

    df1_selected = df1[['Execution#', 'Age', 'Date']].copy()
    df2_selected = df2[['Execution Number', 'Date Received', 'Education Level', 'Date of Offense', 'Prior Occupation', 'Prior Prison Record', 'Summary of Incident']].copy()
    df3_selected = df3[['Execution Number', 'Inmate Name', 'Last Statement']].copy()

    df1_selected.rename(columns={'Execution#': 'Execution Number', 'Date': 'Date Executed'}, inplace=True)
    for df in [df1_selected, df2_selected, df3_selected]:
        df['Execution Number'] = df['Execution Number'].astype(str).str.strip()
    

    combined_df = df1_selected.merge(df2_selected, on='Execution Number', how='outer')
    combined_df = combined_df.merge(df3_selected, on='Execution Number', how='outer')

    complete_info = combined_df.dropna()
    partial_info = combined_df[combined_df.isnull().any(axis=1)]

    final_df = pd.concat([complete_info, partial_info])

    final_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    file1 = 'DATA/deathRowInitial.csv'
    file2 = 'DATA/Clean_Inmate_Info.csv'
    file3 = 'DATA/cleaned_final_statements.csv'
    output_file = 'DATA/Combined_Data.csv'

    combine_csv_files(file1, file2, file3, output_file)
    print(f"Combined data saved to {output_file}")
