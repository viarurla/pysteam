import subprocess

# The following code is a modified version of https://github.com/f0rkz/pysteamcmd
import schemas

generic_failure = "SteamCMD failed."

class SteamCMDException(Exception):
    pass


class SteamCMD(object):
    def __init__(self, install_path):
        self.install_path = install_path

    def soft_login(self, username: str):
        params = [
            "/usr/games/steamcmd",
            f'+login {username}',
            '+quit'
        ]
        try:
            return subprocess.check_call(params)
        except subprocess.CalledProcessError:
            raise SteamCMDException(generic_failure)

    def update_steam(self):
        params = [
            "/usr/games/steamcmd",
            '+quit'
        ]
        try:
            return subprocess.check_call(params)
        except subprocess.CalledProcessError:
            raise SteamCMDException(generic_failure)

    def login(self, login: schemas.LoginRequest):
        params = [
            "/usr/games/steamcmd",
            f'+login {login.user.username}'
            f' {login.password}'
            f' {login.auth}',
            '+quit'
        ]
        try:
            return subprocess.check_call(params)
        except subprocess.CalledProcessError:
            raise SteamCMDException(generic_failure)

    def install_gamefiles(self, request: schemas.DownloadRequest, game_install_dir: str):

        params = [
            "/usr/games/steamcmd",
            f'+@sSteamCmdForcePlatformType {request.platform.lower()}',
            f'+force_install_dir {game_install_dir}',
            f'+login {request.user.username}',
            f'+app_update {request.steam_app.appid}',
            '+quit',
        ]

        try:
            return subprocess.check_call(params)
        except subprocess.CalledProcessError:
            raise SteamCMDException(generic_failure)
