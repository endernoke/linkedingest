from fastapi import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import get_db_connection

def store_cookies(user_id: str, cookie_data: bytes):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO cookies (user_id, cookie_data) VALUES (%s, %s)",
            (user_id, cookie_data)
        )
        conn.commit()
        return {"message": "Cookie stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

def get_cookies(user_id: str) -> dict:
    """
    Return: {"cookie_data": bytes}
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            "SELECT cookie_data FROM cookies WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
            (user_id,)
        )
        result = cur.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Cookie not found")
        return {"cookie_data": result['cookie_data'].tobytes()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
