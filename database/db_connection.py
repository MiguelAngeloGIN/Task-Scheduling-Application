from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("MY_USER")
password = os.getenv("MY_PASSWORD")
database = os.getenv("MY_DATABASE")

engine = create_engine(f"mysql+pymysql://{user}:{password}@localhost/{database}")

conn = engine.connect()

print("✅ Connected!")