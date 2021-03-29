from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PG_DB = 'sweets'
PG_USER = 'postgres'
PG_PASSWORD = 'pgpass'
PG_HOST = '178.154.210.231'
PG_PORT = '8010'

PG_URL = f'''postgresql+psycopg2://{PG_USER}:{PG_PASSWORD
             }@{PG_HOST}:{PG_PORT}/{PG_DB}'''

engine = create_engine(PG_URL, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
