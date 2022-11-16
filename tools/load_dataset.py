
# Usage:
#           python load_dataset.py <filename_1> <filename_2> <filename_3>

import pandas as pd
import sys
import os
from datetime import datetime
#from data.config import POSTGRES_URI
import psycopg2
from sqlalchemy import create_engine
from geopy.geocoders import Nominatim 
import os
from dotenv import load_dotenv
load_dotenv()


POSTGRES_URI = os.getenv("POSTGRES_URI")


if len(sys.argv) != 4:
    print("Error! Missing parametrs: ")
    print("\tpython load_dataset.py <confirmed> <death> <recovered>")
    exit(0)

filename_confirmed = sys.argv[1]
filename_death = sys.argv[2]
filename_recovered = sys.argv[3]

# Open csv files
df_confirmed = pd.read_csv(filename_confirmed)
df_death = pd.read_csv(filename_death)
df_recovered = pd.read_csv(filename_recovered)


# CLEANING DATASET

# Rename columns for simplicity
for df in [df_confirmed, df_death, df_recovered]:
    df.rename(columns = {'Country/Region':'country', 'Province/State':'province', 'Lat':'lat', 'Long':'long'}, inplace=True)


# Generate zones dataframe
df_zones = df_confirmed.groupby(['country'], as_index=False).agg(lambda x: x.iloc[0])


# Regenerate Latitude and Longitude on the following cases:
#   a. They have an invalid value (0 or NaN).
#   b. The latitude refers to a specific province and not the country itself.
rows = df_zones[
    (df_zones['lat'] == 0 ) | (df_zones['long'] == 0) |
    (pd.isna(df_zones['province']) == False)
]

geolocator = Nominatim(user_agent="covid")
for row in rows.iterrows():
    country = row[1]['country']
    location = geolocator.geocode(country)
    df_zones.loc[row[0], ['lat']] = location.latitude
    df_zones.loc[row[0], ['long']] = location.longitude

df_zones = df_zones[['country', 'lat', 'long']]




# Connecting dataframe zones to Postgres
db = create_engine(os.getenv('POSTGRES_URI'))
con = db.connect()
df_zones.to_sql(name='zones', con=con, if_exists='replace')




# Aggregate cases with the same country.
for df in [df_confirmed, df_death, df_recovered]:
    df.drop(['lat', 'long'], axis = 1, inplace=True)
    
df_confirmed = df_confirmed.groupby(['country'], as_index=False).agg('sum')
df_death = df_death.groupby(['country'], as_index=False).agg('sum')
df_recovered = df_recovered.groupby(['country'], as_index=False).agg('sum')


# Generate list of days
days_list = []
for df in [df_confirmed, df_death, df_recovered]:
    days_list += list(df.columns[1:])
days_list = sorted(list(set(days_list)), key=lambda x: datetime.strptime(x, "%m/%d/%y"))


# Generate a list of countries
counties_list = list(df_confirmed['country'])


# Generate a list of cases

cases_list = [] 
for day in days_list:    
    for country in counties_list:
        # TODO: Fill that information from dataframes.
        confirmed = int(df_confirmed.loc[df_confirmed['country'] == country][day])
        death = int(df_death.loc[df_death['country'] == country][day])
        recovered = int(df_recovered.loc[df_recovered['country'] == country][day])
        e = {
            'country': country,
            'day': day,
            'confirmed': confirmed,
            'death': death,
            'recovered': recovered
        }
        cases_list.append(e)

       
# Generate a dataframe of cases
 
df_cases = pd.DataFrame(columns=['country', 'day', 'confirmed', 'death', 'recovered'])

df_cases = pd.DataFrame(cases_list)


# Connecting dataframe cases to Postgres
db = create_engine(os.getenv('POSTGRES_URI'))
con = db.connect()
df_cases.to_sql(name='cases', con=con, if_exists='replace')





exit(0)



# Generate zones dataframe.
df_zones = df_confirmed[['country']]

# Generate latitudes and longitudes for all countries
#df_zones['lat'] = None
#df_zones['long'] = None





geolocator = Nominatim(user_agent="covid")
for row in df_zones.iterrows():
    country = row[1]['country']
    print(country) 
    location = geolocator.geocode(country)
    df_zones.loc[row[0], ['lat']] = location.latitude
    df_zones.loc[row[0], ['long']] = location.longitude  






# Remove the state column

df_confirmed.drop('Province/State', axis = 1, inplace=True)
df_death.drop('Province/State', axis = 1, inplace=True)
df_recovered.drop('Province/State', axis = 1, inplace=True)

# Remove the lat and long column - this information will be placed on the zones dataframe.

df_confirmed.drop(['Lat', 'Long'], axis = 1, inplace=True)
df_death.drop(['Lat', 'Long'], axis = 1, inplace=True)
df_recovered.drop(['Lat', 'Long'], axis = 1, inplace=True)






