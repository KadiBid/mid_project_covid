#!/usr/bin/python

import os
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import json
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


# Connect to db
db = create_engine(os.getenv('POSTGRES_URI'))
con = db.connect()

headers = {'content-type': 'charset=utf-8'}



# Creating API

# Get information (country, lat, long and all cases) from a country id

@app.get("/country/{country_id}")
async def get_country(country_id):
    res = list(con.execute('SELECT * FROM countries WHERE index = %s', (country_id)))
    name = res[0][1]
    data = {
        'id': res[0][0],
        'name': res[0][1],
        'lat': res[0][2],
        'long': res[0][3],
        'cases': [],
    }
    
    res = list(con.execute("SELECT * FROM cases WHERE country = %s", (name)))
    for r in res:
        data['cases'].append({
            'day': r[2],
            'confirmed': r[3],
            'death': r[4],
            'recovered': r[5]
        })
    
    return Response(content=json.dumps(data), media_type="text/json")



# Get cases of a country in a specific day

@app.get("/country/{country_id}/day/{m}/{d}/{y}")
async def get_country_day(country_id, m, d, y):
    res = list(con.execute('SELECT * FROM countries WHERE index = %s', (country_id)))
    name = res[0][1]
    
    res = list(con.execute("SELECT * FROM cases WHERE 'day' = '%s/%s/%s' and country = %s", (m,d,y,name)))
    data = []
    print(res)
    
    for r in res:
        data.append({
            'confirmed': r[3],
            'death': r[4],
            'recovered': r[5]
        })
        
    return Response(content=json.dumps(data), media_type="text/json")




# Get all information about countries

@app.get("/countries/")
async def get_countries():   
    res = list(con.execute("SELECT * FROM countries"))
    data = []
    
    for r in res:
        data.append({
            'id': r[0],
            'name': r[1],
            'lat': r[2],
            'long': r[3]
        })
    
    return Response(content=json.dumps(data), media_type="text/json")



# Get max num of confirmed, death and recovered

@app.get("/max_cases/")
async def get_max_cases():
    max_recov = list(con.execute(f'SELECT MAX(recovered) FROM cases'))
    max_confi = list(con.execute(f'SELECT MAX(confirmed) FROM cases'))
    max_death = list(con.execute(f'SELECT MAX(death) FROM cases'))
    
    max_cases = [ max_confi, max_death, max_recov]

    return Response(content=json.dumps(max_cases), media_type="text/json")


# Get a list of days

@app.get("/list_days/")  
async def get_days():
    res = list(con.execute(f'SELECT DISTINCT day FROM cases'))
    
    data = []
    for r in res:
        data.append(r[0])
    
    return Response(contenct=json.dumpe(data), media_typr="text/json")


