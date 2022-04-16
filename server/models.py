from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    vanity_username = Column(String)
    steamid = Column(Integer, unique=True, nullable=True)
    token = Column(String, nullable=True)

    apps = relationship("SteamApp", backref="owners")


class SteamApp(Base):
    __tablename__ = "steam_apps"

    appid = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    windows = Column(Boolean, default=False)
    mac = Column(Boolean, default=False)
    linux = Column(Boolean, default=False)


class SteamAppInfo(Base):
    __tablename__ = "steam_app_info"

    steam_appid = Column(Integer, unique=True, primary_key=True)
    name = Column(String)
    type = Column(String)
    is_free = Column(Boolean)
    about_the_game = Column(String)
    header_image = Column(String)

    platforms_id = Column(Integer, ForeignKey("platforms.id"))
    platforms = relationship("Platform", foreign_keys=[platforms_id])
