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
import json
import logging
from pydantic.json import pydantic_encoder
from pydantic import TypeAdapter, ValidationError

from repositories.SqlServer import SqlServer
from repositories.Csv import Csv

from services.viewservice import viewservice

from models.novaParams import ParInWithFilter, ParIn, ParOut, ComboOut, Item
from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from utilities.misc import DataSafe

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
    filename="Nova_Server.log",
    encoding="utf-8",
    level=log_level,
)

############################################
# API Authentication
############################################
@router.get("/auth")
async def auth(
    request: Request,
    creds: HTTPBasicCredentials = Depends(basic),
) -> str:
    logger.info(f"auth:start Client Host: '{request.client.host}'")
    # autenticazione
    __authentication(creds)
    # controllo versione
    version: str = __getVersion(request)
    return "OK"


############################################
# API Get Configuration
############################################
@router.get("/")
async def getConfig(
    config: str,
    language: str,
    request: Request,
    creds: HTTPBasicCredentials = Depends(basic),
) -> ParOut:

    logger.info(f"getConfig:start Client Host: '{request.client.host}'")
    # autenticazione
    __authentication(creds)
    # controllo versione
    version: str = __getVersion(request)

    # leggo il file di configurazione
    data = __getData(config)

    title =  DataSafe().getValueString(data, "Title")
    module =  DataSafe().getValueString(data, "Module", "0")

    if module == "1":
        filters =  DataSafe().getValueString(data, "Filters")

    try:
        messages = __get_lang_content(language)
        user_list_adapter = TypeAdapter(list[Item])
        user_list = user_list_adapter.validate_python(messages)
    except ValidationError as e:
        logger.error(e)
        raise HTTPException(status_code=502, detail=e)
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(status_code=502, detail=ex)

    return ParOut(title=title, module=module, findfields=filters, items=user_list)


############################################
# API Laod Combo
############################################
@router.get("/combo")
async def combo(
    config: str,
    language: str,
    request: Request,
    creds: HTTPBasicCredentials = Depends(basic),
) -> ComboOut:
    logger.info(f"combo:start Client Host: '{request.client.host}'")

    # autenticazione
    __authentication(creds)
    # controllo versione
    version: str = __getVersion(request)

    try:
        # leggo il file di configurazione
        data = __getData(config)

        v = viewservice(data)
        return v.loadCombo()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=502, detail=e)


############################################
# API Load Data
############################################
@router.get("/view")
async def get(
    config: str,
    language: str,
    filter: str,
    request: Request,
    creds: HTTPBasicCredentials = Depends(basic),
) -> Any:

    logger.info(f"view:start config:'{config}' language:'{language}'")
    logger.info(f"view:start Client Host: '{request.client.host}'")

    # autenticazione
    __authentication(creds)
    # controllo versione
    version: str = __getVersion(request)

    try:
        # leggo il file di configurazione
        data = __getData(config)

        v = viewservice(data)
        return v.laodView(filter)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=502, detail=e)


############################################
# return configuration data from config file
############################################
def __getData(config):
    try:
        with open("config/" + config, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        logger.error(f"Error in __getData: {str(e)}")
        raise HTTPException(status_code=500, detail=e.args[1])





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

########################################
# menage resource files
########################################
def __get_lang_content(language: str):
    if language.casefold() == "english":
        with open("resources/en.json", "r") as en_file:
            en_data = json.load(en_file)
        return en_data
    elif language.casefold() == "italian":
        with open("resources/it.json", "r") as it_file:
            it_data = json.load(it_file)
        return it_data
    else:
        with open("resources/it.json", "r") as en_file:
            en_data = json.load(en_file)
        return en_data