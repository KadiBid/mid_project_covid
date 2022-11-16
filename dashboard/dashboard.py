
# Usage:
#           python dashboard.py <api_url>

import sys
import pandas as pd
import streamlit as st
import altair as alt
import requests

if len(sys.argv) != 2:
    print("Error! Missing parametrs: ")
    print("\tpython dashboard.py <api_url>")
    exit(0)

api_url = sys.argv[1]



# Get a list of countries and a list of Ids
resp = requests.get(f'{api_url}/countries').json()

countries = {}
for r in resp:
    countries[r['name']] = r


# CONNECT TO STREAMLIT -> 
selected_countries = st.multiselect("Choose stocks to visualize", countries)

for sc in selected_countries:
    country_id = countries[sc]['id']
    resp = requests.get(f'{api_url}/country/{country_id}').json()
    countries[sc]['cases'] = resp['cases']

print(countries)

df_countries = pd.DataFrame(countries)
data1 = alt.Chart(df_countries)

data2 = [
    {"A": [1,2,3,4]},
    {"B": [5,6,7,5,5,10]}
]

st.altair_chart(data1)


exit(0)
# Get list of cases

req = requests.get(f'{api_url}/country/')
req = req.json()


for r in req:
    list_countries.append(r['name'])



# map with countries


# Get a list of cases 
list_cases = []
for country_id in list_id:
    req = requests.get(f'{api_url}/country/{country_id}')
    req = req.json()
    list_cases.append(req['deaths'])