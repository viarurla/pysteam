from typing import List

from sqlalchemy.orm import Session

from server import models, schemas


def drop(db: Session):
    models.SteamApp.__table__.drop(db)
    models.User.__table__.drop(db)


def populate(db: Session, entities: List[any]):
    db.add_all(entities)
    db.commit()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_app(db: Session, app: schemas.SteamAppCreate):
    db_app = models.SteamApp(**app.dict())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def create_apps(db: Session, apps: List[schemas.SteamAppCreate]) -> bool:
    db_apps = [models.SteamApp(**app.dict()) for app in apps]
    db.add_all(db_apps)
    db.commit()
    return True


def set_owned_apps(db: Session, apps: List[schemas.SteamApp]):
    appids = [app.appid for app in apps]
    user_id = apps[0].user_id
    # todo: reset any non-owned values
    db.query(models.SteamApp).filter(models.SteamApp.appid in appids) \
        .update({models.SteamApp.user_id: user_id}, synchronize_session=False)
    db.commit()


def get_apps_like_name(db: Session, name: str, skip: int = 0, limit: int = 100):
    return db.query(models.SteamApp).filter(models.SteamApp.name.ilike(name)).offset(skip).limit(limit).all()


def get_apps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SteamApp).offset(skip).limit(limit).all()


def drop_apps(db: Session) -> bool:
    db.query(models.SteamApp).delete()
    db.commit()
    return len(get_apps(db)) == 0


def get_owned_apps(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.SteamApp).offset(skip).limit(limit).filter(models.SteamApp.user_id == user_id)


def get_app(db: Session, appid: int):
    return db.query(models.SteamApp).get(appid)


def get_app_info(db: Session, appid: int) -> models.SteamAppInfo:
    return db.query(models.SteamAppInfo).join(models.Platform).filter(
        models.SteamAppInfo.steam_appid == appid).first()


def create_app_info(db: Session, info: schemas.SteamAppInfoCreate):
    plat = schemas.PlatformCreate(**info.platforms.dict())
    db_plat = models.Platform(**plat.dict())

    info.platforms = db_plat

    db_info = models.SteamAppInfo(**info.dict())
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info
