#!/usr/bin/python

from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()


@app.get('/')
async def index():
    content = {'mensaje': 'Hola Mundo'}
    return JSONResponse(content=content)



print("Servidor de la API...")