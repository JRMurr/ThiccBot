from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']
DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@postgres:5432/{DB_NAME}'
engine = create_engine(DB_URL, convert_unicode=True)


Base = declarative_base()
Base.metadata.bind = engine
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# We will need this for querying
Base.query = db_session.query_property()
Base.metadata.create_all(engine)