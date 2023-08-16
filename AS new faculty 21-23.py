from pathlib import Path

import pandas as pd

# Define file paths
sas_file_paths = [
    Path('L:\\datalib\\Employees\\edb\\appts2021.sas7bdat'),
    Path('L:\\datalib\\Employees\\edb\\appts2022.sas7bdat'),
    Path('L:\\datalib\\Employees\\edb.def\\appts202301aug.sas7bdat')
]

# Read SAS files into DataFrames
dfs = [pd.read_sas(i, encoding='latin1') for i in sas_file_paths]

# Concatenate DataFrames
df = pd.concat(dfs, ignore_index=True)

# PERS for Hire Date #
sas_file_path = Path('L:\\datalib\\Employees\\edb.def\\pers202301aug.sas7bdat')
pers = pd.read_sas(sas_file_path, encoding='latin1')
pers = pers[['EID','CUHireDate']]

desired_codes = ['1100', '1101', '1102', '1103','1104', '1105', '1106']
columns = (['EID','Year','EmpFirstName', 'EmpLastName','EmpEmail','JobCode','JobTitle','DeptName', 
            'College', 'ASDiv', 'Order','Time'])

# narrow dataframe # 
filtered_df = df[(df['College'] == 'AS') & (df['JobCode'].isin(desired_codes))][columns]

# Add CU Hire Date #
merged_df = pd.merge(filtered_df, pers, on = 'EID', how = 'left')

merged_df['Hire Year'] = merged_df['CUHireDate'].dt.year

df = merged_df[merged_df['Hire Year'] >= 2021]
df = df.sort_values(['EID', 'Year','Order'], ascending=[True, False, True])

dup_criteria = ['EID','JobCode']
as_map = {'NS': 'Natural Sciences',
          'AH': 'Arts & Humanities',
          'SS': 'Social Sciences'}

df_final = df.drop_duplicates(subset = dup_criteria)

df_final['ASDiv'] = df_final['ASDiv'].map(as_map)

columns = (['EID','EmpFirstName','EmpLastName','EmpEmail','JobCode','JobTitle',
            'DeptName','ASDiv','CUHireDate','Hire Year','Time'])

df_final = df_final[columns]
df_final['FTE'] = df_final['Time']

df_final.to_csv('M:\\Decrypt\\as_newfaculty_2123.csv', index = False)
