import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql


DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:123600@localhost:3306/fastapi")

MAX_RETRIES = 5

for retry in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as connection:
            print("Database connection successful.")
        break
    except Exception as e:
        if retry < MAX_RETRIES - 1:
            wait_time = 2 ** retry  # 지수 백오프
            print(f"Database connection failed. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print(f"Database connection failed after {MAX_RETRIES} retries: {e}")
            # 실패해도 계속 진행 (컨테이너 재시작 방지)
            engine = create_engine(DATABASE_URL)

# engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()