from typing import List

from celery.result import AsyncResult
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from services import SteamApiService
import worker as tasks

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:6379",
    "http://localhost:5555",
    "http://localhost:5556",
    "0.0.0.0"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = SteamApiService()
# scs = SteamCmdService()

drop_on_start = True


@app.on_event("startup")
async def startup_event():
    # update_steam_task()
    pass


@app.get("/")
async def root():
    pass


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    return user


@app.get("/users/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@app.get("/apps/{appid}", response_model=schemas.SteamApp)
def get_app(appid: int, db: Session = Depends(get_db)):
    steam_app = crud.get_app(db, appid)
    if steam_app is None:
        raise HTTPException(status_code=404, detail="App not found")
    return steam_app


@app.get("/apps", response_model=List[schemas.SteamApp])
async def get_apps(like: str = None, db: Session = Depends(get_db)):
    if like is not None:
        apps = crud.get_apps_like_name(db, like)
    else:
        apps = crud.get_apps(db)
    return apps


@app.get("/app-info/{appid}", response_model=schemas.SteamAppInfo)
async def get_app_info(appid: int, db: Session = Depends(get_db)):
    info = crud.get_app_info(db, appid)
    if info is None:
        api_info = api.get_app_info(appid)
        info = crud.create_app_info(db, api_info)
    return info


@app.post("/apps/populate/", response_model=bool)
async def update_apps(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    crud.drop_apps(db)
    apps_api = api.get_app_list(user)
    crud.create_apps(db, apps_api)
    return True


@app.post("/apps/set-owned/")
async def update_owned_apps():
    return {"Not": "Implemented"}


@app.post("/soft-login")
async def soft_login(user: schemas.User):
    task = tasks.soft_login_task.delay(user.dict())
    return JSONResponse({"task_id": task.id})


@app.post("/login")
async def login(request: schemas.LoginRequest):
    task = tasks.login_task.delay(request.dict())
    return JSONResponse({"task_id": task.id})


@app.post("/download")
def download(request: schemas.DownloadRequest):
    task = tasks.download_app_task.delay(request.dict())
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JSONResponse(result)
#
#
# @app.post("/login")
# async def login(request: LoginRequest):
#     if len(request.auth) is not 5:
#         return
#     if request.password is None:
#         return
#     result: bool = scs.login(db.get_user(), request.password, request.auth)
#     json_content = jsonable_encoder(result)
#     return JSONResponse(json_content)
