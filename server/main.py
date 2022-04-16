from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from server import crud, models, schemas
from server.database import SessionLocal, engine
from server.services import SteamApiService

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
    app = crud.get_app(db, appid)
    if app is None:
        raise HTTPException(status_code=404, detail="App not found")
    return app


@app.get("/apps", response_model=List[schemas.SteamApp])
async def get_apps(db: Session = Depends(get_db)):
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

# @app.post("/isloggedin")
# async def is_logged_in():
#     result: bool = scs.is_logged_in(db.get_user())
#     json_content = jsonable_encoder(result)
#     return JSONResponse(json_content)
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
