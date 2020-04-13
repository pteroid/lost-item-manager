from app import crud
from app.core import config
from app.schemas.admin import AdminCreate

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.db import base


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    admin = crud.admin.get_by_email(db_session, email=config.FIRST_SUPERUSER)
    if not admin:
        admin_in = AdminCreate(
            email=config.FIRST_SUPERUSER,
            password=config.FIRST_SUPERUSER_PASSWORD,
        )
        admin = crud.admin.create(db_session, obj_in=admin_in)
