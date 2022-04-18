import os
import time

from celery import Celery
from steamcmd import SteamCMD
import schemas

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
output = "/usr/games/"
cmd_path = "/usr/games/steamcmd"
steam = SteamCMD(cmd_path)

# todo: There are some internal imports here that I don't like
# but they avoid a current circular dependency problem.

@celery.task(name="update_steam")
def update_steam_task():
    steam.update_steam()

@celery.task(name="download_app")
def download_app_task(request: dict):
    download_req = schemas.DownloadRequest(**request)
    outdir = os.path.join(output, str(download_req.steam_app.appid))
    steam.install_gamefiles(download_req, outdir)

@celery.task(name="soft_login")
def soft_login_task(request: dict):
    user = schemas.User(**request)
    steam.soft_login(user.username)

@celery.task(name="login")
def login_task(request: dict):
    login_req = schemas.LoginRequest(**request)
    steam.login(login_req)