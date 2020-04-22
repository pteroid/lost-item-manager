from app import crud
from app.core import config
from app.schemas.admin import AdminCreate
from app.schemas.kind import KindCreate
from app.schemas.place import PlaceCreate

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    admin = crud.admin.get_by_email(db_session, email=config.FIRST_SUPERUSER)
    if not admin:
        admin_in = AdminCreate(
            email=config.FIRST_SUPERUSER, password=config.FIRST_SUPERUSER_PASSWORD,
        )
        admin = crud.admin.create(db_session, obj_in=admin_in)

        kinds_ins = [
            KindCreate(name=name)
            for name in (
                "かさ",
                "電子機器",
                "文房具",
                "ノート・ファイル",
                "衣類・タオル",
                "鍵・アクセサリー",
                "教科書・本",
                "その他",
            )
        ]
        crud.kind.create_multi(db_session, obj_ins=kinds_ins)

        place_ins = [
            PlaceCreate(name=name)
            for name in ("AV講義室", "AV演習室", "端末講義室", "端末演習室", "1Fロビー", "2Fロビー")
        ]
        crud.place.create_multi(db_session, obj_ins=place_ins)
