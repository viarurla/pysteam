from server.models import User


class SteamApiEndpoints(object):
    _base_api: str = r"https://api.steampowered.com/"
    _base_store: str = r"https://store.steampowered.com/"

    _resolve_vanity_url: str = r"{base_api}ISteamUser/ResolveVanityURL/v1/?key={key}&vanityurl={username}"
    _get_app_list: str = r"{base_api}ISteamApps/GetAppList/v2/?key={key}"
    _get_owned_games: str = r"{base_api}IPlayerService/GetOwnedGames/v1/?key={key}&steamid={steam_id}"

    _get_app_details:str = r"{base_store}api/appdetails/?appids={appids}"

    def resolve_vanity_url(self, user: User):
        return self._resolve_vanity_url.format(base_api=self._base_api, key=user.token, username=user.vanity_username)

    def get_app_list(self, user: User):
        return self._get_app_list.format(base_api=self._base_api, key=user.token)

    def get_owned_games(self, user: User):
        return self._get_owned_games.format(base_api=self._base_api, key=user.token, steam_id=user.steamid)

    def get_app_details(self, appids: int):
        return self._get_app_details.format(base_store=self._base_store, appids=appids)