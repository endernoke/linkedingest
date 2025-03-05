from pydantic import BaseModel

class RawData(BaseModel):
    profile: dict
    posts: list | None = None

class ProfileResponse(BaseModel):
    full_name: str
    summary: str
    experience: str
    education: str
    honors: str
    certifications: str
    projects: str
    publications: str
    volunteer: str
    skills: str
    languages: str
    posts: str
    raw: RawData
