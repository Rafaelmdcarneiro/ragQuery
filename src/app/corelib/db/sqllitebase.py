from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from corelib.utils.configuration_builder import Settings


class SQLLiteBase():
    """
    This class handled initialization of sqllite database
    """
    __SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = None
    sessionLocal = None
    Base = declarative_base()

    def __init__(self, settings:Settings):
        self.__SQLALCHEMY_DATABASE_URL = settings.sqllite_db_url
        self.engine = create_engine(
            self.__SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        )
        self.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        

  
