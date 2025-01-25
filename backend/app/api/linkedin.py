from ..models.profile import ProfileResponse
from linkedin_api import Linkedin
import dotenv
import os

class LinkedInAgent:
    def __init__(self):
        # get env variables of linkedin credentials
        dotenv.load_dotenv()
        credentials = {
            "username": os.getenv("LINKEDIN_AGENT_USERNAME"),
            "password": os.getenv("LINKEDIN_AGENT_PASSWORD"),
        }
        
        if credentials:
            self.linkedin = Linkedin(credentials["username"], credentials["password"])
        else:
            raise Exception("LinkedIn credentials not provided")
        # print("LinkedIn agent initialized")
    
    def get_profile(self, public_id: str):
        data = self.linkedin.get_profile(public_id)
        if data:
            return data
        else:
            raise Exception("LinkedIn profile not found")
    
    async def get_ingest(self, public_id: str) -> ProfileResponse:
        try:
            raw_data = self.get_profile(public_id)
            profile_data = {
                "user_id": public_id,
                "name": f"{raw_data.get('firstName', '')}{(' ('+raw_data.get('middleName')+')') if raw_data.get('middleName', False) else ''} {raw_data.get('lastName', '')}",
                "profile": raw_data
            }
            return ProfileResponse(**profile_data)
        except Exception as e:
            raise Exception(f"Error fetching LinkedIn profile: {str(e)}")
