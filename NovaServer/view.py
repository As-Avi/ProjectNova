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

router = APIRouter(prefix="/api")

# Basic Auth
secret_user: str = ""
secret_password: str = ""
basic: HTTPBasicCredentials = HTTPBasic()

@router.get("/view")
async def get()->Any:

    df = __loadData()
    return df.to_json(orient='records', compression='gzip')    


def __loadData():
    #df = pd.read_csv("test.csv")
    
    #drivers = pyodbc.drivers()
    cn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};Server=tcp:mkp-devsvr0-eu-ks.8da8c2b450e8.database.windows.net,1433;UID=sqlstgcopy;PWD=***;DATABASE=KeySystems-Customer;')
    cursor = cn.cursor()
    query = "SELECT Id AS ID, Name AS NAME, EmailAddress AS EMAIL FROM dbo.Users ORDER BY Name"
    df = pd.read_sql(query, cn)
    
    #stream = io.StringIO()
    #df.to_csv(stream, sep=',', encoding='utf-8', index=False)
    #stream.seek(0)
    # df = pd.DataFrame(data)

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

