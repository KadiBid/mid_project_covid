
# Usage:
#           python enrich_dataset.py <filename_in> <filename_out>

import pandas as pd
import sys
import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine
from geopy.geocoders import Nominatim 


load_dotenv()

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


# Rename columns for simplicity
df_confirmed.rename(columns = {'Country/Region':'country', 'Province/State':'province', 'Lat':'lat', 'Long':'long'}, inplace=True)
df_death.rename(columns = {'Country/Region':'country', 'Province/State':'province', 'Lat':'lat', 'Long':'long'}, inplace=True)
df_recovered.rename(columns = {'Country/Region':'country', 'Province/State':'province', 'Lat':'lat', 'Long':'long'}, inplace=True)


# Generating zones df.
#df_zones = df_confirmed.groupby(['country', 'province'], as_index=False)[['country', 'province', "lat", "long"]]
df_zones = df_confirmed[['country', 'province', 'lat', 'long']]


# Delete NaNs values in province column (theres's only one: 'Repatriated Travellers')
df_zones = df_zones.dropna(subset = ['lat', 'long'])


# Filing missing latitud and longitud
geolocator = Nominatim(user_agent="covid")


for row in df_zones[(df_zones['lat'] == 0) | (df_zones['long'] == 0)].iterrows():
    province = row[1]['province']
    country = row[1]['country']
    
    if pd.isna(province): 
        location = geolocator.geocode(country)
        df_zones.loc[row[0], ['lat']] = location.latitude
        df_zones.loc[row[0], ['long']] = location.longitude  
    else:
        location = geolocator.geocode(province)
        df_zones.loc[row[0], ['lat']] = location.latitude
        df_zones.loc[row[0], ['long']] = location.longitude



# Connecting to Postgres
db = create_engine(os.getenv('POSTGRES_URI'))
con = db.connect()
df_zones.to_sql(name='zones', con=con, if_exists='replace')