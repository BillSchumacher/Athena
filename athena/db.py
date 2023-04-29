from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
metadata_obj = MetaData()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://athena:athena@localhost:5432/athena"
)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
