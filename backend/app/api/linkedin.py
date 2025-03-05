from ..models.profile import ProfileResponse, RawData
from linkedin_api import Linkedin
from linkedin_api.client import ChallengeException
from linkedin_api.cookie_repository import LinkedinSessionExpired
import dotenv
import os
from datetime import datetime, timedelta
import time
import random
import asyncio
import threading
from typing import Optional, List, Dict, Tuple
import yaml

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
            except Exception as e:
                self.linkedin = None
                raise e
        else:
            raise Exception("LinkedIn credentials not provided")
        print("LinkedIn agent initialized")

        try:
            with open(os.path.join(os.path.dirname(__file__), "../../config.yaml"), "r") as f:
                config = yaml.safe_load(f)
                self.CACHE_ENABLED = config["cache"]["enabled"]
                self.CACHE_TTL_MINUTES = config["cache"]["ttl_minutes"]
                self.DELAY_ON = config["anti_rate_limiting"]["delay"]
                self.MIN_DELAY = config["anti_rate_limiting"]["min_delay"]
                self.MAX_DELAY = config["anti_rate_limiting"]["max_delay"]
                self.NOISE_ON = config["anti_rate_limiting"]["noise"]
                self.NOISE_PROBABILITY = config["anti_rate_limiting"]["noise_probability"]
        except Exception as e:
            print(f"Failed to load config, falling back to default values.\n {repr(e)}")
            self.CACHE_ENABLED = True
            self.CACHE_TTL_MINUTES = 60
            self.DELAY_ON = True
            self.MIN_DELAY = 5
            self.MAX_DELAY = 15
            self.NOISE_ON = True
            self.NOISE_PROBABILITY = 0.3
        
        self._lock = asyncio.Lock()
        self._waiting_requests_count = 0
        self._counter_lock = threading.Lock()

        self._cache: Dict[str, CacheEntry] = {}
        self._cache_lock = threading.Lock()
    
    def _set_counter(self, value: int):
        with self._counter_lock:
            self._waiting_requests_count = value
        
    def get_queue_status(self) -> dict:
        # Overestimate the wait time (in seconds)
        singleWaitTime = 4
        if self.DELAY_ON:
            singleWaitTime += self.MAX_DELAY
        if self.NOISE_ON:
            singleWaitTime += (2 + self.MAX_DELAY) * 0.5 * 2

        return {
            "waiting_requests_count": self._waiting_requests_count,
            "estimated_completion_timestamp": int(time.time()) + (self._waiting_requests_count + 1) * singleWaitTime
        }
    
    def _get_from_cache(self, profile_id: str) -> Optional[ProfileResponse]:
        """Get profile from cache if it exists and is not expired"""
        with self._cache_lock:
            if profile_id in self._cache:
                entry = self._cache[profile_id]
                if not entry.is_expired():
                    print(f"Cache hit for profile {profile_id}")
                    return entry.data
                else:
                    # Remove expired entry
                    print(f"Removing expired cache entry for profile {profile_id}")
                    del self._cache[profile_id]
            return None

    def _add_to_cache(self, profile_id: str, data: ProfileResponse):
        """Add profile data to cache"""
        with self._cache_lock:
            self._cache[profile_id] = CacheEntry(data, self.CACHE_TTL_MINUTES)
            print(f"Added profile {profile_id} to cache")

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
            
            # Pick a noise functions randomly
            selected_funcs = random.sample(noise_funcs, 1)
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
        """
        This method is the main entry point for getting a LinkedIn profile.
        """
        # Skip the queue if the data is already in cache because it does not involve LinkedIn API calls
        if self.CACHE_ENABLED:
            cached_data = self._get_from_cache(public_id)
            if cached_data:
                return cached_data

        self._set_counter(self._waiting_requests_count + 1)
        async with self._lock:
            try:
                profile_response = await self._get_ingest(public_id)
                if self.CACHE_ENABLED:
                    self._add_to_cache(public_id, profile_response)
                self._set_counter(self._waiting_requests_count - 1)
                return profile_response
            except Exception as e:
                self._set_counter(self._waiting_requests_count - 1)
                raise e

    async def _get_ingest(self, public_id: str) -> ProfileResponse:
        print(f"Started fetching LinkedIn profile for {public_id} (is {self._waiting_requests_count-1}th in queue)")
        raw_profile_data = None
        if self.DELAY_ON:
            await self._random_delay()
        try:
            raw_profile_data = self.get_profile(public_id)
            print("Got profile data.")
        except Exception as e:
            print(repr(e))
            raise FetchException("profile")
        
        if self.NOISE_ON:
            await self._make_noise()
        raw_posts_data = None
        try:
            raw_posts_data = self.get_profile_posts(public_id)
            print("Got posts data.")
        except Exception as e:
            print(repr(e))
            # Posts are not critical, so we can continue without them
            raw_posts_data = None
        
        if self.NOISE_ON:
            await self._make_noise()
        
        profile_data = {}
        profile_data["raw"] = RawData(profile=raw_profile_data, posts=raw_posts_data)
        
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
        
        # Posts
        profile_data["posts"] = ""
        try:
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
                    orig_company_name = None
                    if post["actor"]["urn"] != raw_profile_data["member_urn"]:
                        post_type = "repost"
                        if post["actor"]["image"]["attributes"][0].get("miniProfile", False):
                            orig_author = post["actor"]["image"]["attributes"][0]["miniProfile"]
                            orig_author_name = orig_author["firstName"] + " " + orig_author["lastName"]
                            orig_author_headline = orig_author.get("occupation", None)
                        elif post["actor"]["image"]["attributes"][0].get("miniCompany", False):
                            orig_company_name = post["actor"]["image"]["attributes"][0]["miniCompany"].get("name", None)
                    elif post.get("resharedUpdate", False):
                        post_type = "reshare"
                        try:
                            orig_content = post["resharedUpdate"]["commentary"]["text"]["text"]
                        except KeyError:
                            orig_content = None
                        if post["resharedUpdate"]["actor"]["image"]["attributes"][0].get("miniProfile", False):
                            orig_author = post["resharedUpdate"]["actor"]["image"]["attributes"][0]["miniProfile"]
                            orig_author_name = orig_author["firstName"] + " " + orig_author["lastName"]
                            orig_author_headline = orig_author.get("occupation", None)
                        elif post["resharedUpdate"]["actor"]["image"]["attributes"][0].get("miniCompany", False):
                            orig_company_name = post["resharedUpdate"]["actor"]["image"]["attributes"][0]["miniCompany"].get("name", None)
                    
                    num_comments = post["socialDetail"]["totalSocialActivityCounts"]["numComments"]
                    num_shares = post["socialDetail"]["totalSocialActivityCounts"]["numShares"]
                    reactions = post["socialDetail"]["totalSocialActivityCounts"]["reactionTypeCounts"]
                    reaction_str = ", ".join([f"{reaction['count']} ({reaction['reactionType']})" for reaction in reactions])
                    post_content = None
                    try:
                        post_content = post["commentary"]["text"]["text"]
                    except KeyError:
                        post_content = None
                    
                    attribution_prefix = "COMPANY" if orig_company_name else "AUTHOR"
                    if post_type == "post":
                        profile_data["posts"] += "[Posted]\n"
                    if post_type == "reshare":
                        profile_data["posts"] += "[Reshared a post]\n"
                        profile_data["posts"] += f"RESHARED FROM:\n- {attribution_prefix}: {orig_author_name if orig_author_name else orig_company_name}\n"
                        if orig_author_headline:
                            profile_data["posts"] += f"- HEADLINE: {orig_author_headline}\n"
                    if post_type == "repost":
                        profile_data["posts"] += "[Reposted a post]\n"
                        profile_data["posts"] += f"REPOSTED FROM:\n- {attribution_prefix}: {orig_author_name if orig_author_name else orig_company_name}\n"
                        if orig_author_headline:
                            profile_data["posts"] += f"- HEADLINE: {orig_author_headline}\n"
                    profile_data["posts"] += f"REACTIONS: {reaction_str}\n"
                    profile_data["posts"] += f"COMMENTS: {num_comments}\n"
                    profile_data["posts"] += f"SHARES: {num_shares}\n"
                    if post_type == "reshare" and orig_content:
                        profile_data["posts"] += f'ORIGINAL CONTENT:\n"""\n{orig_content}\n"""\n'
                    
                    if post_content:
                        content_prefix = "CONTENT:" if post_type == "post" else "ORIGINAL CONTENT:" if post_type == "repost" else "RESHARE COMMENTARY:"
                        profile_data["posts"] += f'{content_prefix}\n"""\n{post_content}\n"""\n'
                    profile_data["posts"] += "\n"
                profile_data["posts"] = profile_data["posts"][:-2]
        except Exception as e:
            print(f"Failed to process posts: {e}")
            profile_data["posts"] = "# POSTS\nFailed to process posts data\n"
        
        return ProfileResponse(**profile_data)

class CacheEntry:
    def __init__(self, data: ProfileResponse, ttl_minutes: int = 60):
        self.data = data
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(minutes=ttl_minutes)

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at
