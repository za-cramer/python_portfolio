import ada_c2_labs as lab
state_list = lab.fetch_epa('state')
county_list = lab.fetch_epa('county')
aqi_list = lab.fetch_epa('aqi')

epa_tuples = tuple(zip(state_list, county_list, aqi_list))

aqi_dict = {}

for state, county, api in epa_tuples:
    if state in aqi_dict:
        aqi_dict[state].append((county, api))
    else:
        aqi_dict[state] = [(county, api)]

aqi_dict

def readings(state):
    print(len(aqi_dict[state]))
    
readings('Colorado') 
print(type(aqi_dict['California']))

def state_api(state):
    state_aqi = [aqi for county, aqi in aqi_dict[state]]

    state_aqi_total = sum(state_aqi)
    state_aqi_count = len(state_aqi)

    aqi_avg = state_aqi_total / state_aqi_count
    return(aqi_avg)

def county_counter(state):
    lists = []
    for i in range(len(aqi_dict.get(state))):
           lists.append(aqi_dict.get(state)[i][0])
    print(dict((x,lists.count(x)) for x in set(lists)))
    
county_counter('Florida')