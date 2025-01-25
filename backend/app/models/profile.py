from pydantic import BaseModel

class ProfileResponse(BaseModel):
    user_id: str
    name: str
    profile: dict
