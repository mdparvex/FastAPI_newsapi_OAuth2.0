from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time
from app.config import DATABASE_URL

DB_URL = DATABASE_URL


#engine = create_engine(DB_URL)
#Retry connection to avoid tadabase refuge in docker
for i in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        break
    except OperationalError:
        print("Waiting for DB to be ready...")
        time.sleep(2)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()