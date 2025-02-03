from ..models.profile import ProfileResponse
from linkedin_api import Linkedin
from linkedin_api.client import ChallengeException
from linkedin_api.cookie_repository import LinkedinSessionExpired
from ..db.crud import store_cookies, get_cookies
import dotenv
import os
import pickle
from datetime import datetime
import random
import asyncio
from typing import Optional, List, Dict, Any

def remove_file_silently(file_path: str):
    try:
        os.remove(file_path)
    except OSError:
        pass

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

def format_date(date: dict, precision: str = "day") -> str:
    """
    Formats a date object from LinkedIn API into a string in yyyy-mm-dd format.
    "year" is a required field in the date object.
    "month" and "day" are optional fields, they are omitted if not provided (i.e. yyyy-mm or yyyy).
    """
    year = date["year"]
    month = date.get("month", None)
    day = date.get("day", None)
    if precision == "year":
        return f"{year}"
    elif precision == "month":
        return f"{year}-{month:02d}" if month else f"{year}"
    elif precision == "day":
        return f"{year}-{month:02d}-{day:02d}" if month and day else f"{year}-{month:02d}" if month else f"{year}"
    else:
        raise ValueError("Invalid precision value. Must be 'year', 'month', or 'day'.")

def format_duration(timePeriod: dict, startPropName: str = "startDate", endPropName: str = "endDate", prefix: str = "DURATION: ", suffix: str = "\n") -> str:
    """
    Formats a timePeriod object from LinkedIn API into a string in the format "DURATION: yyyy-mm to yyyy-mm" or "DURATION: yyyy-mm to Present".
    """
    start_date = timePeriod.get(startPropName, None)
    end_date = timePeriod.get(endPropName, None)
    # call format_date
    start_str = format_date(start_date, "month") if start_date else "Unknown"
    end_str = format_date(end_date, "month") if end_date else "Present"
    return f"{prefix}{start_str} to {end_str}{suffix}"


class LinkedInAgent:
    MIN_DELAY = 5  # Minimum delay in seconds
    MAX_DELAY = 15  # Maximum delay in seconds
    NOISE_PROBABILITY = 0.3  # 30% chance to make noise requests

    def __init__(self):
        # get env variables of linkedin credentials
        dotenv.load_dotenv()
        credentials = {
            "username": os.getenv("LINKEDIN_AGENT_USERNAME"),
            "password": os.getenv("LINKEDIN_AGENT_PASSWORD"),
        }
        
        if credentials["username"] and credentials["password"]:
            try:
                # Get session cookies
                cookies = get_cookies(credentials["username"])
                print("Got cookies from database")
                cookie_path = os.path.join(os.path.dirname(__file__), f"{credentials["username"]}.jr")
                cookie_dir = os.path.dirname(cookie_path)
                if not cookie_dir.endswith("/"):
                    cookie_dir += "/"
                with open(cookie_path, "wb") as f:
                    f.write(cookies["cookie_data"])
                self.linkedin = Linkedin(credentials["username"], credentials["password"], debug=True, cookies_dir=cookie_dir)
            except LinkedinSessionExpired:
                # Authenticate with username and password and send the new cookies to database
                self.linkedin = Linkedin(credentials["username"], credentials["password"], debug=True, refresh_cookies=True, cookies_dir=cookie_dir)
                cookie_data = pickle.dumps(self.linkedin.client.session.cookies)
                store_cookies(credentials["username"], cookie_data)
                print("Got new cookies and stored them in database")
            except ChallengeException as e:
                self.linkedin = None
                raise e
            except Exception as e:
                self.linkedin = None
                raise e
            finally:
                remove_file_silently(cookie_path)
        else:
            raise Exception("LinkedIn credentials not provided")
        print("LinkedIn agent initialized")
    
    async def _random_delay(self):
        """Add random delay between requests"""
        delay = random.uniform(self.MIN_DELAY, self.MAX_DELAY)
        await asyncio.sleep(delay)

    async def _make_noise(self) -> None:
        """
        Randomly perform noise requests to appear more human-like
        """
        if random.random() < self.NOISE_PROBABILITY:
            noise_funcs = [
                (self.linkedin.get_current_profile_views, {}),
                (self.linkedin.get_invitations, {"start": 0, "limit": 3}),
                (self.linkedin.get_feed_posts, {"limit": 10, "exclude_promoted_posts": True}),
            ]
            
            # Pick 1-2 noise functions randomly
            selected_funcs = random.sample(noise_funcs, random.randint(1, 2))
            for func, kwargs in selected_funcs:
                try:
                    await self._random_delay()
                    func(**kwargs)
                except Exception as e:
                    print(f"Noise request failed (this is fine): {str(e)}")
    
    def get_profile(self, public_id: str):
        if self.linkedin is None:
            raise Exception("LinkedIn agent not initialized")
        data = self.linkedin.get_profile(public_id)
        if data:
            return data
        else:
            raise Exception("LinkedIn profile not found")
    
    def get_profile_posts(self, public_id: str):
        if self.linkedin is None:
            raise Exception("LinkedIn agent not initialized")
        data = self.linkedin.get_profile_posts(public_id)
        if data:
            return data
        else:
            raise Exception("Failed to get profile posts")
    
    async def get_ingest(self, public_id: str) -> ProfileResponse:
        raw_profile_data = None
        await self._random_delay()
        try:
            raw_profile_data = self.get_profile(public_id)
            print("Got profile data.")
        except Exception as e:
            raise FetchException("profile")
        
        await self._make_noise()
        raw_posts_data = None
        try:
            raw_posts_data = self.get_profile_posts(public_id)
            print("Got posts data.")
        except Exception as e:
            raise FetchException("posts")
        await self._make_noise()
        
        profile_data = {}
        
        try:
            profile_data["full_name"] = raw_profile_data["firstName"] + " "
            if raw_profile_data.get("middleName", False):
                profile_data["full_name"] += raw_profile_data["middleName"] + " "
            profile_data["full_name"] += raw_profile_data["lastName"]

            # Summary
            profile_data["summary"] = f"PROFILE OF: {profile_data["full_name"]}\n"
            if raw_profile_data.get("headline", "--") != "--":
                profile_data["summary"] += f"HEADLINE: {raw_profile_data["headline"]}\n"
            profile_data["summary"] += f"LOCATION: {f"{raw_profile_data["geoLocationName"]}, " if raw_profile_data.get("geoLocationName", False) else ""}{raw_profile_data.get("geoCountryName", "")}\n"
            if raw_profile_data.get("summary", False):
                profile_data["summary"] += f'\n# ABOUT\n"""\n{raw_profile_data["summary"]}\n"""\n'
            profile_data["summary"] = profile_data["summary"][:-1] # remove the last newline character

            # Experience
            profile_data["experience"] = ""
            if raw_profile_data.get("experience", False):
                profile_data["experience"] = "# EXPERIENCES\n"
                for experience in raw_profile_data["experience"]:
                    if is_ongoing(experience):
                        profile_data["experience"] += "[Current]\n"
                    else:
                        profile_data["experience"] += "[Previous]\n"
                    profile_data["experience"] += f"{experience['title']}"
                    if experience.get("companyName", False):
                        profile_data["experience"] += f" at {experience['companyName']}"
                    profile_data["experience"] += "\n"
                    if experience.get("timePeriod", False):
                        profile_data["experience"] += format_duration(experience["timePeriod"])
                    
                    if experience.get("description", False):
                        profile_data["experience"] += f'DESCRIPTION:\n"""\n{experience["description"]}\n"""\n'
                    profile_data["experience"] += "\n"
                profile_data["experience"] = profile_data["experience"][:-2]

            # Education
            profile_data["education"] = ""
            if raw_profile_data.get("education", False):
                profile_data["education"] = "# EDUCATION\n"
                for education in raw_profile_data["education"]:
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
                        profile_data["education"] += format_duration(education["timePeriod"])

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
            if raw_profile_data.get("projects", False):
                profile_data["projects"] = "# PROJECTS\n"
                for project in raw_profile_data["projects"]:
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
                        profile_data["projects"] += format_duration(project["timePeriod"])
                    
                    if project.get("description", False):
                        profile_data["projects"] += f'DESCRIPTION:\n"""\n{project["description"]}\n"""\n'
                    profile_data["projects"] += "\n"
                profile_data["projects"] = profile_data["projects"][:-2]

            # Honors
            profile_data["honors"] = ""
            if raw_profile_data.get("honors", False):
                profile_data["honors"] = "# HONORS\n"
                for honor in raw_profile_data["honors"]:
                    profile_data["honors"] += f"NAME: {honor['title']}\n"
                    if honor.get("issuer", False):
                        profile_data["honors"] += f"ISSUED BY: {honor['issuer']}\n"
                    if honor.get("issueDate", False):
                        profile_data["honors"] += f"ISSUE DATE: {format_date(honor['issueDate'])}\n"
                    
                    if honor.get("description", False):
                        profile_data["honors"] += f'DESCRIPTION:\n"""\n{honor["description"]}\n"""\n'
                    profile_data["honors"] += "\n"
                profile_data["honors"] = profile_data["honors"][:-2]
            
            # Skills
            profile_data["skills"] = ""
            if raw_profile_data.get("skills", False):
                profile_data["skills"] = "# SKILLS\n"
                skills_list = [skill["name"] for skill in raw_profile_data["skills"]]
                profile_data["skills"] += ", ".join(skills_list)
            
            # Languages
            profile_data["languages"] = ""
            if raw_profile_data.get("languages", False):
                profile_data["languages"] = "# LANGUAGES\n"
                for language in raw_profile_data["languages"]:
                    profile_data["languages"] += language['name']
                    if language.get("proficiency", False):
                        profile_data["languages"] += f" ({language['proficiency']})"
                    profile_data["languages"] += ", "
                
                profile_data["languages"] = profile_data["languages"][:-2]
            
            # Certifications
            profile_data["certifications"] = ""
            if raw_profile_data.get("certifications", False):
                profile_data["certifications"] = "# LICENSES AND CERTIFICATIONS\n"
                for certification in raw_profile_data["certifications"]:
                    profile_data["certifications"] += f"NAME: {certification['name']}\n"
                    if certification.get("authority", False):
                        profile_data["certifications"] += f"ISSUED BY: {certification['authority']}\n"
                    if certification.get("timePeriod", False):
                        profile_data["certifications"] += f"ISSUE DATE: {format_date(certification["timePeriod"]["startDate"])}\n"
                    if certification.get("description", False):
                        profile_data["certifications"] += f'DESCRIPTION:\n"""\n{certification["description"]}\n"""\n'
                    profile_data["certifications"] += "\n"
                profile_data["certifications"] = profile_data["certifications"][:-2]

            # Publications
            profile_data["publications"] = ""
            if raw_profile_data.get("publications", False):
                profile_data["publications"] = "# PUBLICATIONS\n"
                for publication in raw_profile_data["publications"]:
                    profile_data["publications"] += f"TITLE: {publication['name']}\n"
                    if publication.get("authors", False):
                        num_authors = len(publication.get("authors", [True]))
                        profile_data["publications"] += f"AUTHORS: {profile_data['full_name']}{f' and {num_authors - 1} other(s)' if num_authors > 1 else ''}\n"
                    
                    if publication.get("date", False):
                        profile_data["publications"] += f"PUBLICATION DATE: {format_date(publication['date'])}\n"
                    if publication.get("description", False):
                        profile_data["publications"] += f'DESCRIPTION:\n"""\n{publication["description"]}\n"""\n'
                    profile_data["publications"] += "\n"
                profile_data["publications"] = profile_data["publications"][:-2]

            # Volunteer
            profile_data["volunteer"] = ""
            if raw_profile_data.get("volunteer", False):
                profile_data["volunteer"] = "# VOLUNTEER\n"
                for volunteer in raw_profile_data["volunteer"]:
                    if is_ongoing(volunteer):
                        profile_data["volunteer"] += "[Current]\n"
                    else:
                        profile_data["volunteer"] += "[Previous]\n"
                    
                    profile_data["volunteer"] += f"{volunteer['role']} at {volunteer['companyName']}\n"
                    if volunteer.get("cause", False):
                        profile_data["volunteer"] += f"CAUSE: {volunteer['cause']}\n"
                    if volunteer.get("timePeriod", False):
                        profile_data["volunteer"] += format_duration(volunteer["timePeriod"])
                    if volunteer.get("description", False):
                        profile_data["volunteer"] += f'DESCRIPTION:\n"""\n{volunteer["description"]}\n"""\n'
                    profile_data["volunteer"] += "\n"
                profile_data["volunteer"] = profile_data["volunteer"][:-2]
        
        except Exception as e:
            print(e)
            raise ParseException(f"Error while processing LinkedIn profile: {str(e)}")
        
        # TODO: Add posts and recommendations
        try:
            # Posts
            profile_data["posts"] = ""
            if raw_posts_data:
                profile_data["posts"] = "# POSTS\n"
                for post in raw_posts_data:
                    # Here:
                    #   "post" is a post that the user has created themselves;
                    #   "repost" is a post that the user has reposted from another user without any additional commentary;
                    #   "reshare" is a post that the user has reposted from another user with additional commentary;
                    # If the post is a "repost", the LinkedIn API directly gives us the original data in the post object. Everything is linked to the original post.
                    # If the post is a "reshare", he LinkedIn API gives us the original post data in the "resharedUpdate" field.
                    # This is not yet confirmed to be the general case, but it seems to be true for the posts tested so far.
                    post_type = "post"
                    orig_content = ""
                    orig_author = None
                    orig_author_name = None
                    orig_author_headline = None
                    if post["actor"]["urn"] != raw_profile_data["member_urn"]:
                        post_type = "repost"
                        orig_author = post["actor"]["image"]["attributes"][0]["miniProfile"]
                        orig_author_name = orig_author["firstName"] + " " + orig_author["lastName"]
                        orig_author_headline = orig_author.get("occupation", None)
                    elif post.get("resharedUpdate", False):
                        post_type = "reshare"
                        orig_content = post["resharedUpdate"]["commentary"]["text"]["text"]
                        orig_author = post["resharedUpdate"]["actor"]["image"]["attributes"][0]["miniProfile"]
                        orig_author_name = orig_author["firstName"] + " " + orig_author["lastName"]
                        orig_author_headline = orig_author.get("occupation", None)
                    
                    num_comments = post["socialDetail"]["totalSocialActivityCounts"]["numComments"]
                    num_shares = post["socialDetail"]["totalSocialActivityCounts"]["numShares"]
                    reactions = post["socialDetail"]["totalSocialActivityCounts"]["reactionTypeCounts"]
                    reaction_str = ", ".join([f"{reaction['count']} ({reaction['reactionType']})" for reaction in reactions])
                    post_content = post["commentary"]["text"]["text"]
                    
                    if post_type == "post":
                        profile_data["posts"] += "[Posted]\n"
                    if post_type == "reshare":
                        profile_data["posts"] += "[Reshared a post]\n"
                        profile_data["posts"] += f"RESHARED FROM:\n- NAME: {orig_author_name}\n"
                        if orig_author_headline:
                            profile_data["posts"] += f"- HEADLINE: {orig_author_headline}\n"
                    if post_type == "repost":
                        profile_data["posts"] += "[Reposted a post]\n"
                        profile_data["posts"] += f"REPOSTED FROM:\n- NAME: {orig_author_name}\n"
                        if orig_author_headline:
                            profile_data["posts"] += f"- HEADLINE: {orig_author_headline}\n"
                    profile_data["posts"] += f"REACTIONS: {reaction_str}\n"
                    profile_data["posts"] += f"COMMENTS: {num_comments}\n"
                    profile_data["posts"] += f"SHARES: {num_shares}\n"
                    if post_type == "reshare":
                        profile_data["posts"] += f'ORIGINAL CONTENT:\n"""\n{orig_content}\n"""\n'
                    
                    content_prefix = "CONTENT:" if post_type == "post" else "ORIGINAL CONTENT:" if post_type == "repost" else "RESHARE COMMENTARY:"
                    profile_data["posts"] += f'{content_prefix}\n"""\n{post_content}\n"""\n'
                    profile_data["posts"] += "\n"
                profile_data["posts"] = profile_data["posts"][:-2]
            
        except Exception as e:
            print(e)
            raise ParseException(f"Error while processing LinkedIn posts: {str(e)}")
        
        return ProfileResponse(**profile_data)