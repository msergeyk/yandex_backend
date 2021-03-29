import os
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PG_DB = 'sweets'
PG_USER = os.getenv('POSTGRES_USER')
PG_PASSWORD = os.getenv('POSTGRES_PASSWORD')
PG_HOST = os.getenv('POSTGRES_HOST')
PG_PORT = os.getenv('POSTGRES_PORT')

PG_URL = f'''postgresql+psycopg2://{PG_USER}:{PG_PASSWORD
             }@{PG_HOST}:{PG_PORT}/{PG_DB}'''

engine = create_engine(PG_URL, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
