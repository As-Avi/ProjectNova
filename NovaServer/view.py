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
from dotenv import load_dotenv
import time
import pandas as pd
import pyodbc
import json
import logging

router = APIRouter(prefix="/api")

load_dotenv()

# Basic Auth
secret_user: str = ""
secret_password: str = ""
basic: HTTPBasicCredentials = HTTPBasic()

log_level = int(os.getenv("LOG_LEVEL"))

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filename="Novi_server.log",
    encoding="utf-8",
    level=log_level
)


@router.get("/view")
async def get(
    config, language, request: Request, creds: HTTPBasicCredentials = Depends(basic)
) -> Any:

    logger.info(f"view:start config:'{config}' language:'{language}'")
    logger.info(f"view:start Client Host: '{request.client.host}'")

    # autenticazione
    __authentication(creds)
    # controllo versione
    version: str = __getVersion(request)

    # leggo il file di configurazione
    with open("config/" + config, "r") as file:
        data = json.load(file)

    type = data["Type"]
    logger.info(f"view:{type}")

    if type == "SqlServer":
        df = __loadDataSqlServer(data)
    elif type == "CSV":
        df = __loadDataCSV(data)
    else:
        logger.error(f"Wrong Type")
        raise HTTPException(status_code=502, detail="Wrong Type")

    if df is None:
        logger.error(f"Empty Data Frame")
        raise HTTPException(status_code=501, detail="Empty Data Frame")

    logger.info("view:end")

    return df.to_json(orient="records")


def __loadDataCSV(data):
    return pd.read_csv("data/" + data["File"])  # da migliorare gestione errore


def __loadDataSqlServer(data):
    try:
        connectionString = data["ConnectionString"]
        query = data["Query"]

        logger.info(f"__loadDataSqlServer:{connectionString}")
        logger.info(f"__loadDataSqlServer:{query}")
        # drivers = pyodbc.drivers()
        cn = pyodbc.connect(connectionString)
        cursor = cn.cursor()

        df = pd.read_sql(
            query, cn
        )  # warning perchè Sql server non è un database nativo di pandas (usare SQLAlchemy)
        return df
    except Exception as e:
        logger.error(f"Error in __loadDataSqlServer: {str(e)}")
        raise HTTPException(status_code=500, detail=e.args[1])

    return df


########################################
# authentication
########################################
def __authentication(creds: HTTPBasicCredentials):
    secret_user = os.getenv("USER")
    secret_password = os.getenv("PWD")

    if (
        creds.username.casefold() != secret_user.casefold()
        or creds.password != secret_password
    ):
        logger.error(f"Incorrect username or password")
        raise HTTPException(status_code=401, detail="Incorrect username or password")


########################################
# get API version
########################################
def __getVersion(request: Request) -> str:
    version = request.headers.get("header-version")
    if version is None:
        version = "1.0"

    return version