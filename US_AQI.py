'''
In your work as an analyst, you are continuing your research into air quality data collected by the U.S. Environmental Protection Agency (EPA). 
The air quality index (AQI) is a number that runs from 0 to 500. 
The higher the AQI value, the greater the level of air pollution and the greater the health concern.
'''

# Import Files for Lab #
import ada_c2_labs as lab
state_list = lab.fetch_epa('state')
county_list = lab.fetch_epa('county')
aqi_list = lab.fetch_epa('aqi')

# Convert lists into a list of tuples #
epa_tuples = tuple(zip(state_list, county_list, aqi_list))

'''
Convert epa_tuples into a dictionary.
State: key; county & aqi: values
'''
# Instantiate aqi_dictionary
aqi_dict = {}

for state, county, api in epa_tuples:
    if state in aqi_dict:
        aqi_dict[state].append((county, api))
    else:
        aqi_dict[state] = [(county, api)]

aqi_dict

# Define function to calculate # of readings for state specified
def readings(state):
    print(len(aqi_dict[state]))
    
readings('Colorado') 
print(type(aqi_dict['California']))

# Define function to calculate average API readings for state specified
def state_api(state):
    state_aqi = [aqi for county, aqi in aqi_dict[state]]

    state_aqi_total = sum(state_aqi)
    state_aqi_count = len(state_aqi)

    aqi_avg = state_aqi_total / state_aqi_count
    return(aqi_avg)

# Define Function to county how many readings per county occured within a given state
def county_counter(state):
    lists = []
    for i in range(len(aqi_dict.get(state))):
           lists.append(aqi_dict.get(state)[i][0])
    print(dict((x,lists.count(x)) for x in set(lists)))
    
county_counter('Florida')
