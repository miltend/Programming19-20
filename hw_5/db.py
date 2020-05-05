from sqlalchemy import create_engine, Column, Integer, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from config import Config
from logs import get_logger
import sys

Base = declarative_base()

logger = get_logger(__name__)


def make_engine():
    try:
        config = Config()
    except ValueError as exc:
        logger.exception(f"could not read config: {exc}")
        sys.exit(1)

    try:
        engine = create_engine(config.dsn)
        engine.execute("SELECT 1")
    except Exception as exc:
        logger.exception(f"could not connect to db: {exc}")
        sys.exit(1)

    return engine


def init_db():
    engine = make_engine()
    Base.metadata.create_all(engine)


class DB_model(Base):
    __tablename__ = 'learning'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    given_data_param = Column(JSONB, nullable=False)
    model_inf = Column(JSONB, nullable=False)
    cv_results = Column(JSONB, nullable=False)
    ready = Column(Boolean, default=False)

