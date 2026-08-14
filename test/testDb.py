from sqlalchemy import text
from db.database import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1")).scalar()
    print("Database connection successful!")
    print("Result:", result)