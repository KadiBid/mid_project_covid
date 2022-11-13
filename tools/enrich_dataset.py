
# Usage:
#           python enrich_dataset.py <filename_in> <filename_out>

import pandas as pd
import sys
import streamlit as st
from geopy.geocoders import Nominatim


if len(sys.argv) != 3:
    print("Error! Missing parametrs: ")
    print("\tpython enrich_dataset.py <filename_in> <filename_out>")
    exit(0)

filename_in = sys.argv[1]
filename_out = sys.argv[2]



# Open csv file
df = pd.read_csv(filename_in)

# Remove the state column.
df = df.drop('Province/State', axis = 1)
df = df.drop('Lat', axis = 1)
df = df.drop('Long', axis = 1)

# Aggregate cases with the same country.
df = df.groupby(['Country/Region'], as_index=False).agg('sum')

# Generate a list with all countries
list_countries = list(df['Country/Region'])

# Streamlit

# Creat a multiselect
countries = st.multiselect("Choose stocks to visualize", list_countries)




st.line_chart(data=df, y = 'Country/Region', x = countries)
