# https://github.com/za-cramer/python_portfolio/blob/main/football_stats.py #

import pprint

import pandas as pd
import requests
from bs4 import BeautifulSoup

standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

# make request to url server to access HTML of page #
data = requests.get(standings_url)

# Initialize 'soup' using Beautiful Soup
soup = BeautifulSoup(data.text)

# From webpage, use the inspector to parse desired HTML elements #
# What we're looking for are the individual club's URLs denoted by the <a tag. 
#   within the table (a stats_table element)

# retreive the first stats_table element in the list #
standings_table = soup.select('table.stats_table')[0]

# find atags by find_all #
links = standings_table.find_all('a')

# get href property for each link #
links_href = []
for i in links:
    links_href.append(i.get("href"))
pprint.pprint(links_href)

# filter to retain squad links #
links_squad =[]
for i in links_href:
    if '/squads/' in i:
        links_squad.append(i)

pprint.pprint(links_squad)
print(len(links_squad))

# make links into full urls using format string #
team_urls = [] 
for i in links_squad:
    team_urls.append(f"https://fbref.com{i}")

###################################################
# retrieve a team's data #
team_url = team_urls[0]
team_data = requests.get(team_url)

# data #
matches = pd.read_html(team_data.text, match="Scores & Fixtures")[0]
print(matches)

# shooting data #
soup = BeautifulSoup(team_data.text)

links = soup.find_all('a')

linksb = [] 
for i in links:
    linksb.append(i.get("href"))

pprint.pprint(linksb)
shooting_links = []
for i in linksb:
    if i and 'all_stats_shooting' in i:
        shooting_links.append(i)
    

shooting_data_url = requests.get(f"https://fbref.com{shooting_links[0]}")

# read html with pandas #
shooting = pd.read_html(shooting_data_url.text, match="Shooting")[0]
shooting.columns = shooting.columns.droplevel()

# two DF. Matches & Shooting #
team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
pprint.pprint(team_data)
