from typing import List

import requests

from server import schemas
from server.settings import SteamApiEndpoints


class SteamApiService(object):

    def __init__(self):
        self._endpoints = SteamApiEndpoints()

    def get_steam_id(self, user: schemas.User):
        r = requests.get(self._endpoints.resolve_vanity_url(user=user))
        return r.json()['response']['steamid']

    def get_app_list(self, user: schemas.User) -> List[schemas.SteamAppCreate]:
        apps: List[schemas.SteamAppCreate] = []
        r = requests.get(self._endpoints.get_app_list(user))
        for record in r.json()['applist']['apps']:
            apps.append(schemas.SteamAppCreate(**record))

        return apps

    def get_owned_apps(self, user: schemas.User) -> List[schemas.SteamApp]:
        apps: List[schemas.SteamApp] = []
        r = requests.get(self._endpoints.get_owned_games(user))
        for record in r.json()['response']['games']:
            apps.append(schemas.SteamApp(**{"steamid": user.steamid, **record}))
        return list(set(apps))

    def get_app_info(self, appid: int) -> schemas.SteamAppInfoCreate:
        endpoint: str = self._endpoints.get_app_details(appid)
        r = requests.get(endpoint)

        record = r.json()[str(appid)]
        if record['success'] is not False:
            app_details = schemas.SteamAppInfoCreate(**record['data'])
            return app_details

