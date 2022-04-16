import sys
import os
import platform
import zipfile
import tarfile
import subprocess
from pathlib import Path

from urllib.request import urlretrieve


# The following code is a modified version of https://github.com/f0rkz/pysteamcmd
from server import schemas


class SteamcmdException(Exception):

    pass


class Steamcmd(object):
    def __init__(self, install_path):

        self.install_path = install_path
        if not os.path.isdir(self.install_path):
            raise SteamcmdException('Install path is not a directory or does not exist: {}'.format(self.install_path))

        self.platform = platform.system()
        if self.platform == 'Windows':
            self.steamcmd_exe = Path(self.install_path, 'steamcmd.exe')

        elif self.platform == 'Linux':
            self.steamcmd_exe = Path(self.install_path, 'steamcmd.sh')

        elif self.platform == "Darwin":
            self.steamcmd_exe = Path(self.install_path, 'steamcmd.sh')

        else:
            raise SteamcmdException(
                'The operating system is not supported. Expected Linux or Windows, received: {}'.format(self.platform)
            )

    def soft_login(self, username: str):
        params = [
            self.steamcmd_exe,
            f'+login {username}',
            '+quit'
        ]
        try:
            return subprocess.check_call(params)
        except subprocess.CalledProcessError:
            raise SteamcmdException("Steamcmd was unable to run. Did you install your 32-bit libraries?")

    def login(self, user: schemas.User, creds: schemas.LoginRequest):
        params = [
            self.steamcmd_exe,
            f'+login {user.username}',
            f'{creds.password}',
            f'{creds.auth}'
            '+quit'
        ]
        try:
            return subprocess.check_call(params)
        except subprocess.CalledProcessError:
            raise SteamcmdException("Steamcmd was unable to run. Did you install your 32-bit libraries?")

    def install_gamefiles(self, username: str, gameid, game_install_dir, validate=False):
        if validate:
            validate = 'validate'
        else:
            validate = None

        params = [
            self.steamcmd_exe,
            f'+force_install_dir {game_install_dir}',
            f'+login {username}',
            f'+app_update {gameid}',
            f'{validate}',
            '+quit',
        ]

        try:
            return subprocess.check_call(params)
        except subprocess.CalledProcessError:
            raise SteamcmdException("Steamcmd was unable to run. Did you install your 32-bit libraries?")
