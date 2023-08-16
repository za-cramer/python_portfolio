from pathlib import Path

import pandas as pd

sas_file_path = Path('L:\\datalib\\Employees\\edb\\appts2021.sas7bdat')
df21 = pd.read_sas(sas_file_path, encoding='latin1')

sas_file_path = Path('L:\\datalib\\Employees\\edb\\appts2022.sas7bdat')
df22 = pd.read_sas(sas_file_path, encoding='latin1')

sas_file_path = Path('L:\\datalib\\Employees\\edb.def\\appts202301aug.sas7bdat')
df23 = pd.read_sas(sas_file_path, encoding='latin1')

sas_file_path = Path('L:\\datalib\\Employees\\edb.def\\pers202301aug.sas7bdat')
pers = pd.read_sas(sas_file_path, encoding='latin1')

pers = pers[['EID','CUHireDate']]

df = pd.concat([df21, df22, df23], ignore_index=True)

desired_codes = ['1100', '1101', '1102', '1103','1104', '1105', '1106']
columns = (['EID','Year','EmpFirstName', 'EmpLastName','JobCode','JobTitle','DeptName', 
            'College', 'ASDiv', 'Order','Time'])

# narrow dataframe # 
filtered_df = df[(df['College'] == 'AS') & (df['JobCode'].isin(desired_codes))][columns]
filtered_df

df = df[columns] # for all appts for FTE #

# Add CU Hire Date #
merged_df = pd.merge(filtered_df, pers, on = 'EID', how = 'left')

merged_df['Hire Year'] = merged_df['CUHireDate'].dt.year

# Calculate FTE by Year #
FTE = df.groupby(['EID', 'Year'])['Time'].sum().reset_index()
FTE['Total Time'] = FTE['Time']
FTE = FTE.drop('Time',axis = 1)

merged_df_fte = pd.merge(merged_df, FTE, on = ['EID','Year'], how = 'left')

df = merged_df_fte[merged_df_fte['Hire Year'] >= 2021]
df = df.sort_values(['EID', 'Year','Order'])

dup_criteria = ['EID','JobCode']

df_final = df.drop_duplicates(subset = dup_criteria)
df_final[['Hire Year','JobTitle']].value_counts()