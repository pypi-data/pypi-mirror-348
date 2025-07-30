from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker
import logging
from dotenv import load_dotenv
import os
load_dotenv()
from securities.logs import SessionLogging

echo_all = SessionLogging()
database_ur = os.environ.get('POSTGRES_KEY')
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING) 

load_dotenv("/app/.env")
 
database_ur = os.environ.get("DATABASE_URL") 
if not database_ur:
    raise ValueError("DATABASE_URL environment variable is not set")
echo=True
 

engine = create_engine(database_ur,
    pool_size=90,  # Increase pool size
    max_overflow=30,  # Increase overflow limit
    pool_timeout=60,  # Increase timeout if needed
    pool_pre_ping=True,
    echo=echo_all 
    )

# Dependency to get DB session (using SQLModel.Session)
def get_db():
    db = Session(engine)  # Use Session from SQLModel
    try:
        yield db
    finally:
        db.close()
