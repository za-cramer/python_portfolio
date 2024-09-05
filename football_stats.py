import pprint
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
