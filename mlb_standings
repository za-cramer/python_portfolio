import statsapi
from datetime import datetime
import pprint
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Get today's date in the desired format
today = datetime.today().strftime("%m/%d/%Y")

# Retrieve standings data for today
standings_df = statsapi.standings_data(date = today)

# Import Team Colors (https://github.com/rhelmstedter/coding-class/blob/main/coding-projects/data/mlb.csv)#
colors_csv = 'c:\\xxx\\xxx\\xxx\\mlb.csv'
colors = pd.read_csv(colors_csv)
# Update Indians to Guardians #
colors.loc[4,'team'] = 'Guardians'

colors['Team'] = colors['location'] + ' ' + colors['team'] 
colors = colors.drop(['location', 'team'], axis = 1)

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

# Add Colors #
df = df.merge(colors, on='Team',how = 'left')
df
# Show Updated Date #
df['Updated_Last'] = today

# Sort #
df = df.sort_values('Wins', ascending = False).reset_index(drop = True)

# Create the figure and axis
fig, ax = plt.subplots()

# Set the bar positions
x = range(len(df))
bar_width = 0.5

# Create the bar chart
bars = ax.bar(x, df['Wins'], width=bar_width, color=df['primary_color'])

# Add labels and titles
ax.set_ylabel('Wins')
ax.set_title(f'Team Wins ({today})')

# Add data labels to the bars
for i, bar in enumerate(bars):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            df['Wins'].iloc[i], ha='center', va='bottom')

# Set the x-axis tick labels to the team names
ax.set_xticks(x)
ax.set_xticklabels(df['Team'], rotation=45, ha='right')

# Show the chart
plt.tight_layout()
plt.show()
