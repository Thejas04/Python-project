from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

ENGINE = None

def get_connection() -> Engine:
    global ENGINE
    if ENGINE is None:
        ENGINE = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    return ENGINE
