import numpy as np
import pandas as pd

# Load your CSV file
df = pd.read_csv('data/survey.csv')

df.head()
df.info()

    # Identify all columns that contain the word 'Comment'
comment_columns = [col for col in df.columns if 'Comment' in col]
   # Identify all columns that contain the word 'Rating'
rating_columns = [col for col in df.columns if 'Rating' in col]

df[rating_columns] = df[rating_columns].apply(pd.to_numeric, errors='coerce')

    # Create a flag column for respondents who left any non-'No Response' and non-NaN comment
df['Comment_Flag'] = df[comment_columns].apply(
    lambda row: any(comment not in ['No Response', np.nan] and pd.notna(comment) for comment in row), axis=1
        )

    # Sum all 'Rating' fields
df['Rating_Sum'] = df[rating_columns].sum(axis=1)
    
df = df.sort_values(by = ['Rating_Sum'], ascending = [True])

df['Rating_Sum'].max()

df.to_csv('product/cleaned_survey.csv', index=False)
