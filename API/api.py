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
