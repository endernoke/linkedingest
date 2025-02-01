import linkedin_api.utils
from ..models.profile import ProfileResponse
from linkedin_api import Linkedin
from linkedin_api.client import ChallengeException
import dotenv
import os
from datetime import datetime

class FetchException(Exception):
    pass
class ParseException(Exception):
    pass

def is_ongoing(experience: dict) -> bool:
    if experience.get("timePeriod", False) == False:
        return True
    if experience["timePeriod"].get("endDate", False) == False:
        return True
    end_date = experience["timePeriod"]["endDate"]
    end_year = end_date["year"]
    end_month = end_date.get("month", 12)  # Default to December if month is not provided
    if datetime(end_year, end_month, 1) < datetime.now():
        return False
    else:
        return True

class LinkedInAgent:
    def __init__(self):
        # get env variables of linkedin credentials
        dotenv.load_dotenv()
        credentials = {
            "username": os.getenv("LINKEDIN_AGENT_USERNAME"),
            "password": os.getenv("LINKEDIN_AGENT_PASSWORD"),
        }
        
        if credentials["username"] and credentials["password"]:
            try:
                self.linkedin = Linkedin(credentials["username"], credentials["password"], debug=True)
            except ChallengeException as e:
                self.linkedin = None
                raise e
        else:
            raise Exception("LinkedIn credentials not provided")
        print("LinkedIn agent initialized")
    
    def get_profile(self, public_id: str):
        if self.linkedin is None:
            raise Exception("Could not perform LinkedIn API calls. Please contact the maintainer if this issue persists.")
        data = self.linkedin.get_profile(public_id)
        if data:
            return data
        else:
            raise Exception("LinkedIn profile not found")
    
    async def get_ingest(self, public_id: str) -> ProfileResponse:
        raw_data = None
        try:
            raw_data = self.get_profile(public_id)
            print("Got raw data.")
        except Exception as e:
            raise FetchException()
        
        try:
            profile_data = {}
            profile_data["full_name"] = raw_data["firstName"] + " "
            if raw_data.get("middleName", False):
                profile_data["full_name"] += raw_data["middleName"] + " "
            profile_data["full_name"] += raw_data["lastName"]

            # Summary
            profile_data["summary"] = f"PROFILE OF: {profile_data["full_name"]}\n"
            if raw_data.get("headline", "--") != "--":
                profile_data["summary"] += f"HEADLINE: {raw_data["headline"]}\n"
            profile_data["summary"] += f"LOCATION: {f"{raw_data["geoLocationName"]}, " if raw_data.get("geoLocationName", False) else ""}{raw_data.get("geoCountryName", "")}\n"
            if raw_data.get("summary", False):
                profile_data["summary"] += f'\n# ABOUT\n"""\n{raw_data["summary"]}\n"""\n'
            profile_data["summary"] = profile_data["summary"][:-1] # remove the last newline character

            # Experience
            profile_data["experience"] = ""
            if raw_data.get("experience", False):
                profile_data["experience"] = "# EXPERIENCES\n"
                for experience in raw_data["experience"]:
                    if is_ongoing(experience):
                        profile_data["experience"] += "[Current]\n"
                    else:
                        profile_data["experience"] += "[Previous]\n"
                    profile_data["experience"] += f"{experience['title']}"
                    if experience.get("companyName", False):
                        profile_data["experience"] += f" at {experience['companyName']}"
                    profile_data["experience"] += "\n"
                    if experience.get("timePeriod", False):
                        start_date = experience["timePeriod"]["startDate"] # Must be present
                        start_year = start_date["year"]
                        start_month = start_date.get("month", 1)
                        end_date = experience["timePeriod"].get("endDate", None)
                        if end_date:
                            end_year = end_date["year"]
                            end_month = end_date.get("month", 12)
                        profile_data["experience"] += f"DURATION: {start_year}-{start_month:02d} to {f"{end_year}-{end_month:02d}" if end_date is not None else "Present"}\n"
                    
                    if experience.get("description", False):
                        profile_data["experience"] += f'DESCRIPTION:\n"""\n{experience["description"]}\n"""\n'
                    profile_data["experience"] += "\n"
                profile_data["experience"] = profile_data["experience"][:-2]

            # Education
            profile_data["education"] = ""
            if raw_data.get("education", False):
                profile_data["education"] = "# EDUCATION\n"
                for education in raw_data["education"]:
                    if is_ongoing(education):
                        profile_data["education"] += "[Current]\n"
                    else:
                        profile_data["education"] += "[Previous]\n"
                    
                    profile_data["education"] += f"INSTITUTION: {education['schoolName']}\n"
                    if education.get("degreeName", False):
                        profile_data["education"] += f"DEGREE: {education['degreeName']}\n"
                    if education.get("fieldOfStudy", False):
                        profile_data["education"] += f"FIELD OF STUDY: {education['fieldOfStudy']}\n"
                    
                    if education.get("timePeriod", False):
                        start_date = education["timePeriod"]["startDate"]
                        start_year = start_date["year"]
                        start_month = start_date.get("month", 1)
                        end_date = education["timePeriod"].get("endDate", None)
                        if end_date:
                            end_year = end_date["year"]
                            end_month = end_date.get("month", 12)
                        profile_data["education"] += f"Duration: {start_year}-{start_month:02d} to {f"{end_year}-{end_month:02d}" if end_date is not None else "Present"}\n"

                    if education.get("grade", False):
                        profile_data["education"] += f"GRADE: {education['grade']}\n"
                    if education.get("activities", False):
                        profile_data["education"] += f'ACTIVITIES AND SOCIETIES:\n"""\n{education['activities']}\n"""\n'
                    if education.get("description", False):
                        profile_data["education"] += f'DESCRIPTION:\n"""\n{education["description"]}\n"""\n'
                    
                    profile_data["education"] += "\n"
                profile_data["education"] = profile_data["education"][:-2]

            # Projects
            profile_data["projects"] = ""
            if raw_data.get("projects", False):
                profile_data["projects"] = "# PROJECTS\n"
                for project in raw_data["projects"]:
                    if is_ongoing(project):
                        profile_data["projects"] += "[Current]\n"
                    else:
                        profile_data["projects"] += "[Previous]\n"

                    profile_data["projects"] += f"NAME: {project["title"]}\n"
                    num_members = len(project.get("members", [True])) # Min number of members is 1
                    profile_data["projects"] += f"MEMBERS: {profile_data["full_name"]}"
                    if num_members > 1:
                        profile_data["projects"] += f" and {num_members - 1} other(s)"
                    profile_data["projects"] += "\n"

                    if project.get("timePeriod", False):
                        start_date = project["timePeriod"]["startDate"]
                        start_year = start_date["year"]
                        start_month = start_date.get("month", 1)
                        end_date = project["timePeriod"].get("endDate", None)
                        if end_date:
                            end_year = end_date["year"]
                            end_month = end_date.get("month", 12)
                        profile_data["projects"] += f"Duration: {start_year}-{start_month:02d} to {f"{end_year}-{end_month:02d}" if end_date is not None else "Present"}\n"
                        
                    if project.get("description", False):
                        profile_data["projects"] += f'DESCRIPTION:\n"""\n{project["description"]}\n"""\n'
                    profile_data["projects"] += "\n"
                profile_data["projects"] = profile_data["projects"][:-2]

            # Honors
            profile_data["honors"] = ""
            if raw_data.get("honors", False):
                profile_data["honors"] = "# HONORS\n"
                for honor in raw_data["honors"]:
                    profile_data["honors"] += f"NAME: {honor['title']}\n"
                    if honor.get("issuer", False):
                        profile_data["honors"] += f"ISSUED BY: {honor['issuer']}\n"
                    if honor.get("issueDate", False):
                        issue_date = honor["issueDate"]
                        issue_year = issue_date["year"]
                        issue_month = issue_date.get("month", 1)
                        profile_data["honors"] += f"ISSUE DATE: {issue_year}-{issue_month:02d}\n"
                    if honor.get("description", False):
                        profile_data["honors"] += f'DESCRIPTION:\n"""\n{honor["description"]}\n"""\n'
                    profile_data["honors"] += "\n"
                profile_data["honors"] = profile_data["honors"][:-2]
            
            # Skills
            profile_data["skills"] = ""
            if raw_data.get("skills", False):
                profile_data["skills"] = "# SKILLS\n"
                skills_list = [skill["name"] for skill in raw_data["skills"]]
                profile_data["skills"] += ", ".join(skills_list)
            
            # Languages
            profile_data["languages"] = ""
            if raw_data.get("languages", False):
                profile_data["languages"] = "# LANGUAGES\n"
                for language in raw_data["languages"]:
                    profile_data["languages"] += f"{language['name']}: {language['proficiency']}\n"
                profile_data["languages"] = profile_data["languages"][:-1]
            
            # Certifications
            profile_data["certifications"] = ""
            if raw_data.get("certifications", False):
                profile_data["certifications"] = "# LICENSES AND CERTIFICATIONS\n"
                for certification in raw_data["certifications"]:
                    profile_data["certifications"] += f"NAME: {certification['name']}\n"
                    if certification.get("authority", False):
                        profile_data["certifications"] += f"ISSUED BY: {certification['authority']}\n"
                    if certification.get("timePeriod", False):
                        issue_date = certification["timePeriod"]["startDate"]
                        issue_year = issue_date["year"]
                        issue_month = issue_date.get("month", 1)
                        profile_data["certifications"] += f"ISSUE DATE: {issue_year}-{issue_month:02d}\n"
                    if certification.get("description", False):
                        profile_data["certifications"] += f'DESCRIPTION:\n"""\n{certification["description"]}\n"""\n'
                    profile_data["certifications"] += "\n"
                profile_data["certifications"] = profile_data["certifications"][:-2]

            # Publications
            profile_data["publications"] = ""
            if raw_data.get("publications", False):
                profile_data["publications"] = "# PUBLICATIONS\n"
                for publication in raw_data["publications"]:
                    profile_data["publications"] += f"TITLE: {publication['name']}\n"
                    if publication.get("authors", False):
                        num_authors = len(publication.get("authors", [True]))
                        profile_data["publications"] += f"AUTHOR(S): {profile_data['full_name']}{f' and {num_authors - 1} other(s)' if num_authors > 1 else ''}\n"

                    if publication.get("date", False):
                        publication_date = publication["date"]
                        publication_year = publication_date["year"]
                        publication_month = publication_date.get("month", None)
                        publication_day = publication_date.get("day", None)
                        profile_data["publications"] += f"PUBLICATION DATE: {publication_year}{f"-{publication_month:02d}" if publication_month else ""}{f"-{publication_day:02d}" if publication_day else ""}\n"
                    if publication.get("description", False):
                        profile_data["publications"] += f'DESCRIPTION:\n"""\n{publication["description"]}\n"""\n'
                    profile_data["publications"] += "\n"
                profile_data["publications"] = profile_data["publications"][:-2]

            # Volunteer
            profile_data["volunteer"] = ""
            if raw_data.get("volunteer", False):
                profile_data["volunteer"] = "# VOLUNTEER\n"
                for volunteer in raw_data["volunteer"]:
                    if is_ongoing(volunteer):
                        profile_data["volunteer"] += "[Current]\n"
                    else:
                        profile_data["volunteer"] += "[Previous]\n"
                    
                    profile_data["volunteer"] += f"{volunteer['role']} at {volunteer['companyName']}\n"
                    if volunteer.get("cause", False):
                        profile_data["volunteer"] += f"CAUSE: {volunteer['cause']}\n"
                    
                    if volunteer.get("timePeriod", False):
                        start_date = volunteer["timePeriod"]["startDate"]
                        start_year = start_date["year"]
                        start_month = start_date.get("month", 1)
                        end_date = volunteer["timePeriod"].get("endDate", None)
                        if end_date:
                            end_year = end_date["year"]
                            end_month = end_date.get("month", 12)
                        profile_data["volunteer"] += f"Duration: {start_year}-{start_month:02d} to {f"{end_year}-{end_month:02d}" if end_date is not None else "Present"}\n"

                    if volunteer.get("description", False):
                        profile_data["volunteer"] += f'DESCRIPTION:\n"""\n{volunteer["description"]}\n"""\n'
                    profile_data["volunteer"] += "\n"
                profile_data["volunteer"] = profile_data["volunteer"][:-2]

            # TODO: Add posts and recommendations
            # (we might need to call a different api function for this)
            
            return ProfileResponse(**profile_data)
        except Exception as e:
            print(e)
            raise ParseException(f"Error fetching LinkedIn profile: {str(e)}")
