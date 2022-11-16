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

@app.get('/')
async def index():
    content = {'mensaje': 'COVID Analysis'}
    return JSONResponse(content=content, headers = headers)

print("Servidor de la API...")


@app.get("/html/")
def html():
    content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>COVID Analysis</title>
    </head>
    <body>
        <h1>COVID Analysis</h1>
    </body>
    </html>
    """
    return Response(content=content, media_type="text/html")



# Get information (country, lat, long, all cases) from a country id

@app.get("/country/{country_id}")
async def get_country(country_id):
    res = list(con.execute(f'SELECT * FROM countries WHERE index = {country_id}'))
    name = res[0][1]
    data = {
        'id': res[0][0],
        'name': res[0][1],
        'lat': res[0][2],
        'long': res[0][3],
        'cases': []
    }

    res = list(con.execute(f"SELECT * FROM cases WHERE country = '{name}'"))
    for r in res:
        data['cases'].append({
            'day': r[2],
            'confirmed': r[3],
            'death': r[4],
            'recovered': r[5]
        })
    
    return Response(content=json.dumps(data), media_type="text/json")


@app.get("/country/{country_id}/day/{d}/{m}/{y}")
async def get_country_day(country_id, d, m, y):
    return

# Get all information about countries

@app.get("/countries/")
async def get_countries():   
    res = list(con.execute(f"SELECT * FROM countries"))
    data = []
    
    for r in res:
        data.append({
            'id': r[0],
            'name': r[1],
            'lat': r[2],
            'long': r[3]
        })
    
    return Response(content=json.dumps(data), media_type="text/json")