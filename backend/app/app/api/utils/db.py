from app.db.session import Session


# Dependsで用いる場合、暗黙的にcontextmanagerでデコレートされる
def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
