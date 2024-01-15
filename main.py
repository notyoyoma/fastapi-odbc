import logging
import pyodbc

from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

import uvicorn
app = FastAPI()

@app.get("/")
@cache(namespace="run", expire=5)
async def index():
    logging.warning("RUNNING index()")
    connection_string_parts = [
        "DRIVER={Devart ODBC Driver for SQL Server}"
        "Server="
        "Database="
        "Port="
        "User ID="
        "Password="
    ]
    connection = pyodbc.connect(";".join(connenction_string_parts))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM table ORDER BY date LIMIT 1000")
    return cursor.fetchall()

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
