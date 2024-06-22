from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# use with sqlite
SQLALCHEMY_DATABASE_URL = "sqlite:///./garmin.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# use with mysql
# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:password@10.9.8.221:3306/garminApplicationDatabase'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
