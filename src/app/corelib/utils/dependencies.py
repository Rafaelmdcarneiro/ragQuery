from functools import lru_cache
from typing import List
from corelib.utils.configuration_builder import Settings, TestSettings
from corelib.utils.logger_factory import LoggerFactory
from typing_extensions import Annotated
from fastapi import Depends, Request
from corelib.db.sqllitebase import SQLLiteBase

@lru_cache
def get_settings()->Settings: 
    return Settings()

@lru_cache
def get_test_settings()->TestSettings: 
    return TestSettings()

def create_logger(settings:Annotated[Settings, Depends(get_settings)]):
    lg = LoggerFactory()
    return LoggerFactory().get_logger(settings)


def get_sqllite_db(settings:Annotated[Settings, Depends(get_settings)]):
    db_base = SQLLiteBase(settings=settings)
    session = db_base.sessionLocal()
    try:
        yield session
    finally:
        session.close()