from fastapi import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import dotenv

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cookies (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255),
                cookie_data BYTEA,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cur.close()
        conn.close()
