from fastapi import FastAPI, APIRouter, Request, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse, FileResponse

from typing import Optional

import os

from app.db.db import db

from app.middleware.authorizationCheck.authorization_check import authorization_check as __authorization_check__
from app.middleware.Logging.logging import logging as __logging__

from app.endpoints.postFile.post_file import post_file as __post_file__
from app.endpoints.getFile.get_file import get_file as __get_file__
from app.endpoints.getFileHeaders.get_file_headers import get_file_headers as __get_file_headers__

# IMPORTS
#
#
# APP INIT

app = FastAPI()
app_router = APIRouter()

# APP INIT
#
#
# DB MAGIC

@app_router.on_event("startup")
async def startup():
    if not db.is_connected:
        await db.connect()

@app_router.on_event("shutdown")
async def shutdown():
    if db.is_connected:
        await db.disconnect()


# DB MAGIC
# 
#
# MIDDLEWARE
#TODO rewrite ALL middleware initialization as a Factory method (template?)


#Consuming request body inside of the middleware currently does not work, look https://github.com/encode/starlette/issues/495, https://github.com/tiangolo/fastapi/issues/394. Until changed, do via router instead

async def authorization_check(request: Request):
    res = await __authorization_check__(request)
    request.state.auth = res

async def logging(request: Request):
    await __logging__(request)

# MIDDLEWARE
#
#
# PATHES

@app_router.post("/files")
async def post_file(request: Request, uploaded_file: UploadFile = File(...), auth_token: str = Form(None)):
    if bool(request.state.auth):
        res = await __post_file__(uploaded_file)
        return JSONResponse(status_code=res, content={"message": "Something went wrong" if res != 201 else "Created!"}) #TODO list every exception separately
    else:
        return JSONResponse(status_code=403, content={"message": "Forbbiden!"})

@app_router.get("/files/{id}")
async def get_file(request: Request, id: int, auth_token: str = Form(None)):
    if bool(request.state.auth):
        res = await __get_file__(id)
        if type(res) is int:
            return JSONResponse(status_code=res, content={"message": "Something went wrong"}) #TODO list every exception separately
        else:
            return FileResponse(res[0], filename=res[1])
    else:
        return JSONResponse(status_code=403, content={"message": "Forbbiden!"})

@app_router.head("/files/{id}") # I'm not sure what was meant by "information about the file", responding with file size and creation time as an example
async def get_file_headers(request: Request, id: int): # auth_token: str = Form(None)): //Can't have auth check with HEAD request
    #if bool(request.state.auth):
    res = await __get_file_headers__(id)
    if type(res) is int:
        request.state.error_status_code = res
        #return JSONResponse(status_code=res, content={"message": "Something went wrong"}) # no responses on HEAD
    else:
        setattr(request.state, "X-file_size", res[0])
        setattr(request.state, "X-file_saved_at", res[1])

    #else:
    #    return JSONResponse(status_code=403, content={"message": "Forbbiden!"})

app.include_router(app_router, dependencies=[Depends(authorization_check), Depends(logging)])
