from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
import secrets
import dotenv
import os

security = HTTPBasic()

def setup_admin():
    global ADMIN_USERNAME, ADMIN_PASSWORD
    dotenv.load_dotenv()
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def authenticate_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Authenticates the user as an administrator."""
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True  # Indicate successful authentication
