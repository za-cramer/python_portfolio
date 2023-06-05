import statsapi
from datetime import datetime
import pprint
import pandas as pd

# Get today's date in the desired format
today = datetime.today().strftime("%m/%d/%Y")

# Retrieve standings data for today
standings_df = statsapi.standings_data(date = today)

# Define a list of divisions
divisions = [200, 201, 202, 203, 204, 205]

# Initialize empty lists to store team names, wins, and losses
team_names = []
win = []
loss = []

# Extract team names, wins, and losses from the standings data
for i in divisions:
    for team in standings_df[i]['teams']:
        team_names.append(team['name'])
        win.append(team['w'])
        loss.append(team['l'])

# Create a dictionary with team names, wins, and losses
df = {'Team': team_names, 'Wins': win, 'Losses': loss}

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

# Show Updated Date #
df['Updated_Last'] = today

pprint.pprint(df)