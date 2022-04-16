from pydantic import BaseModel


class LoginRequest(BaseModel):
    password: str
    auth: str


class SteamAppBase(BaseModel):
    appid: int
    name: str


class SteamAppCreate(SteamAppBase):
    pass


class SteamApp(SteamAppBase):
    user_id: int = None
    class Config:
        orm_mode = True


class PlatformBase(BaseModel):
    windows: bool
    mac: bool
    linux: bool


class PlatformCreate(PlatformBase):
    pass


class Platform(PlatformBase):
    id: int

    class Config:
        orm_mode = True


class SteamAppInfoBase(BaseModel):
    steam_appid: int
    name: str
    type: str
    is_free: bool
    about_the_game: str | None = None
    header_image: str | None = None

class SteamAppInfoCreate(SteamAppInfoBase):
    platforms: PlatformCreate

class SteamAppInfo(SteamAppInfoBase):
    platforms: Platform

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    vanity_username: str = None
    token: str = None
    steamid: str = None


class User(UserBase):
    id: int
    token: str
    apps: list[SteamApp] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass
