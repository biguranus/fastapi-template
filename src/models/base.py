# # -*- coding:utf-8 -*-
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from src.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ENGINE_OPTIONS

__all__ = ["db"]


class _SQLAlchemy:
    def __init__(self):
        self.Model = declarative_base()
        self.session = self.get_session_factory()

    @staticmethod
    def get_engine():
        return create_engine(
            SQLALCHEMY_DATABASE_URI,
            pool_size=SQLALCHEMY_ENGINE_OPTIONS["pool_size"],
            pool_recycle=SQLALCHEMY_ENGINE_OPTIONS["pool_recycle"],
            pool_timeout=SQLALCHEMY_ENGINE_OPTIONS["pool_timeout"],
        )

    def get_session_factory(self):
        session_factory = sessionmaker(bind=self.get_engine(), expire_on_commit=False)
        return scoped_session(session_factory)

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise


db = _SQLAlchemy()
