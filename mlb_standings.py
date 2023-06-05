import statsapi
from datetime import datetime
import pprint
import pandas as pd
import numpy as np

# Get today's date in the desired format
today = datetime.today().strftime("%m/%d/%Y")

# Retrieve standings data for today
standings_df = statsapi.standings_data(date = today)
pprint.pprint(standings_df)
# Define a list of divisions
divisions = [200, 201, 202, 203, 204, 205]

# Initialize empty lists to store team names, wins, and losses
team_names = []
win = []
loss = []
div_rank = []

# Extract team names, wins, and losses from the standings data
for i in divisions:
    for team in standings_df[i]['teams']:
        team_names.append(team['name'])
        win.append(team['w'])
        loss.append(team['l'])
        div_rank.append(team['div_rank'])

# Create a dictionary with team names, wins, and losses
df = {'Team': team_names, 'Wins': win, 'Losses': loss, 'Divisional Rank': div_rank}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(df)

# Map team names to their respective divisions using a dictionary
team_divisions = {}

for key, value in standings_df.items():
    teams = value['teams']
    for team in teams:
        team_name = team['name']
        div_name = value['div_name']
        team_divisions[team_name] = div_name

# Add a 'Division' column to the DataFrame using .map() method
df['Division'] = df['Team'].map(team_divisions)

# Add AL or NL - using Lambda#
#df['new column name'] = df['column name'].apply(lambda x: 'value if condition is met' if x condition else 'value if condition is not met')#
df['League'] = df['Division'].apply(lambda x: 'AL' if 'American League' in x else 'NL')

# Add Winning or Losing Record - using Lambda #
df['Record'] = np.where(df['Wins'] > df['Losses'], 'Winning',
                        np.where(df['Wins'] < df['Losses'], 'Losing',
                                 np.where(df['Wins'] == df['Losses'], '.500', None)))
# Show Updated Date #
df['Updated_Last'] = today

# Sort #
df = df.sort_values('Wins', ascending = False).reset_index(drop = True)
pprint.pprint(df)
df.info()
