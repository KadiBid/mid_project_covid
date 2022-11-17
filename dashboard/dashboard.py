
# Usage:
#           python dashboard.py <api_url>

import sys
import os
import pandas as pd
import streamlit as st
import altair as alt
import requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
import numpy as np


if len(sys.argv) != 2:
    print("Error! Missing parametrs: ")
    print("\tpython dashboard.py <api_url>")
    exit(0)

api_url = sys.argv[1]
# http://localhost:8000

st.title('COVID dashboard')
st.text("Showing COVID data") 


# Get a list of countries and a list of Ids
resp = requests.get(f'{api_url}/countries').json()

countries = {}
for r in resp:
    countries[r['name']] = r
    

# CONNECT TO STREAMLIT -> 
selected_country = st.multiselect("Choose stocks to visualize", countries)


# Show cases about country selected

countries_with_cases = {}
for sc in selected_country:
    country_id = countries[sc]['id']
    resp = requests.get(f'{api_url}/country/{country_id}').json()
    countries[sc]['cases'] = resp['cases']
    countries[sc]['confirmed'] = resp['confirmed']
    # this a list of {day:... , confirmed: ... , death: ... , recovered: ...}
    # here countries = a lis of countries info and cases of the selected country
    
    day = []
    for dict in resp['day']:
        day.append(dict['day'])
     
    confirmed = []
    for dict in resp['confirmed']:
        confirmed.append(dict['confirmed'])
    
    deaths = []
    for dict in resp['deaths']:
        deaths.append(dict['deaths'])
    
    recovered = []
    for dict in resp['recovered']:
        recovered.append(dict['recovered'])
        
    datos = [range(len(day)), confirmed, deaths, recovered]
    df = pd.DataFrame(datos)
    
    c = alt.Chart(df).mark_circle().encode(
    x='day', y='cases', tooltip=['day', 'cases'])


    st.altair_chart(c, use_container_width=True)



exit(0)
df = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['a', 'b', 'c'])

c = alt.Chart(df).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.altair_chart(c, use_container_width=True)


exit(0)

resp = requests.get(f'{api_url}/max_cases/').json()
max_confi = resp[0]
max_death = resp[1]
max_recov = resp[2]




df_countries = pd.DataFrame(countries)
data1 = alt.Chart(df_countries).mark_circle().encode(
)

# Get list of cases

req = requests.get(f'{api_url}/country/')
req = req.json()


list_cases = []
for country_id in list_id:
    req = requests.get(f'{api_url}/country/{country_id}').json()
    list_cases.append(req['deaths'])
    
    

# map with countries


