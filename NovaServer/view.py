import string
from fastapi import Depends, FastAPI, Body, Response, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import PlainTextResponse
from fastapi import APIRouter
from fastapi.responses import Response
from typing import Union
from typing import Any
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import requests
from pathlib import Path
import uvicorn
import os, errno
import time
import pandas as pd
import pyodbc
import json

router = APIRouter(prefix="/api")

# Basic Auth
secret_user: str = ""
secret_password: str = ""
basic: HTTPBasicCredentials = HTTPBasic()

@router.get("/view")
async def get(config, language)->Any:

    #leggo il file di configurazione
    with open('config/' + config, 'r') as file:
        data = json.load(file)

    if data['Type'] == 'SqlServer':
        df = __loadDataSqlServer(data)
    elif data['Type'] == 'CSV':
        df = __loadDataCSV(data)
    else:
        return None #da migliorare gestione errore

    return df.to_json(orient='records', compression='gzip')    

def __loadDataCSV(data):
    return  pd.read_csv("data/" + data['File']) #da migliorare gestione errore

def __loadDataSqlServer(data):
    try:
        #drivers = pyodbc.drivers()
        cn = pyodbc.connect(data['ConnectionString'])
        cursor = cn.cursor()
        query = data['Query']
        df = pd.read_sql(query, cn)
        return df
    except Exception as e:
        sqlstate = e.args[0]
        print(e.args[1])
        return None

    return df


########################################
# authentication
########################################
def __authentication(creds: HTTPBasicCredentials):
    if (
        creds.username.casefold() != secret_user.casefold()
        or creds.password != secret_password
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")


########################################
# get API version
########################################
def __getVersion(request: Request) -> str:
    version = request.headers.get("header-version")
    if version is None:
        version = "1.0"

    return version

