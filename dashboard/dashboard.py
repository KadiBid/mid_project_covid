
# Usage:
#           python dashboard.py <api_url>

import sys
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
import altair as alt
import requests

if len(sys.argv) != 2:
    print("Error! Missing parametrs: ")
    print("\tpython dashboard.py <api_url>")
    exit(0)

api_url = sys.argv[1]
# http://localhost:8000

st.title('COVID dashboard')
st.text("Showing COVID data") 


# Get all countries
resp = requests.get(f'{api_url}/countries').json()

all_countries = {}
for r in resp:
    all_countries[r['name']] = r
       
# Creating multiselect bar
multiselect_countries = st.multiselect("Choose countries to visualize", all_countries, ['Spain'])


# Get all information about countries, included cases
df_list = []

selected_countries = {}
for country in multiselect_countries:
    country_id = all_countries[country]['id']
    selected_countries[country] = requests.get(f'{api_url}/country/{country_id}').json()

    # Creating dataframe per country
    df = pd.DataFrame(selected_countries[country]['cases'])
    df['country'] = selected_countries[country]['name']
    df['current_day'] = False
    df.iloc[-1, df.columns.get_loc('current_day')] = True
    df_list.append(df)


# Creating one dataframe with all dataframes
df_all = pd.concat(df_list, ignore_index=True)


# Create a box with types of cases
cases_type = st.selectbox("Select type of cases", ['confirmed', 'death', 'recovered'])


# Creating Chart
chart = (
    alt.Chart(df_all)
    .mark_line()
    .encode(
        x = 'day:T',
        y = f'{cases_type}:Q',
        color = 'country:N'))

st.altair_chart(chart, use_container_width=True)


# Creating a Mark Char with total data about countries

df_current_day = df_all[df_all['current_day'] == True]
    
chart = (alt.Chart(df_current_day)
         .mark_circle()
         .encode(
             x = 'confirmed', 
             y = 'death',
             tooltip=['country', 'confirmed', 'death']))

st.altair_chart(chart, use_container_width=True)





# Map
# Center on country, add marker


st.title('COVID World Map')

show_all_countries = st.checkbox("show all countries", value=False)

if show_all_countries:
    df_list = []
    for country in all_countries:
        country_id = all_countries[country]['id']
        print(all_countries[country])
        
        resp = requests.get(f'{api_url}/country/{country_id}')
        print(resp.text)
        
        all_countries[country] = requests.get(f'{api_url}/country/{country_id}').json()
        
        df = pd.DataFrame(all_countries[country]['cases'])
        df['country'] = all_countries[country]['name']
        df['current_day'] = False
        df.iloc[-1, df.columns.get_loc('current_day')] = True
        df_list.append(df)
    df_all = pd.concat(df_list, ignore_index=True)
    
    df_current_day = df_all[df_all['current_day'] == True]   

country_shapes = requests.get("https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json").json()

map = folium.Map()

M=1000000
folium.Choropleth(
    geo_data=country_shapes,
    data=df_current_day,
    columns=['country', 'confirmed'],
    key_on='feature.properties.name',
    fill_color='YlGn',
    highlight = True,
    bins=[0, 2.5*M,  5*M, 7.5*M, 10*M, 20*M, 30*M, 40*M],
    nan_fill_color='grey'
).add_to(map),

folium_static(map)

