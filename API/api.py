#!/usr/bin/python

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

headers = {'content-type': 'charset=utf-8'}
app = FastAPI()


@app.get('/')
async def index():
    content = {'mensaje': 'COVID Analisis'}
    return JSONResponse(content=content, headers = headers)

print("Servidor de la API...")


@app.get('/html/')
def html():
    content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>COVID Analisis</title>
    </head>
    <body>
        <h1>COVID Analisis</h1>
    </body>
    </html>
    """
    return Response(content=content, media_type="text/html")

