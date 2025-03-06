<div align="center">
  <h1 align="center">LinkedIngest</h1>

  <p align="center">
    Turn LinkedIn profiles into AI-friendly text ingests.
    <br />
    <a href="https://linkedingest.onrender.com">View Demo</a>
    ·
    <a href="https://github.com/endernoke/linkedingest/issues/new?template=bug_report.md">Report Bug</a>
    ·
    <a href="https://github.com/endernoke/linkedingest/issues/new?template=feature_request.md">Request Feature</a>
  </p>
</div>


https://github.com/user-attachments/assets/87f1dab4-c7fa-4b39-8842-94859116fc87


## About The Project

LinkedIngest is a web application that converts LinkedIn profiles into structured text format optimized for feeding to Large Language Models (LLMs). It extracts comprehensive profile information including:
- Basic info (name, headline, location)
- Experience history
- Education background
- Projects
- Skills & Languages
- Certifications
- Publications
- Volunteer work
- Recent posts and activities

The extracted data is formatted in a clean, consistent markdown-like text structure that's ideal for LLM ingestion.

## Usage

There are two ways to access someone's profile ingest:
- **Direct URL Access**: Replace `linkedin.com` with `linkedingest.onrender.com` (or whatever URL you hosted it on) in any LinkedIn profile URL:
   ```
   https://linkedin.com/in/john-doe-123 → https://linkedingest.onrender.com/in/john-doe-123
   ```

- **Search by ID**: Enter a LinkedIn profile ID in the search bar:
   ```
   john-doe-123
   ```

Click on any of the example profiles provided on the homepage to see how the app works.

The generated text output can be:
- Copied entirely or by sections
- Downloaded as a text file
- Used directly with any LLM

### Example Use Cases

Here are some example use cases for LinkedIngest:

- **Writing Engaging Invitations**
  Quickly analyze LinkedIn profiles to craft personalized and engaging connection requests or messages.
- **Networking**
  Prepare for networking events by summarizing the profiles of attendees, helping you to make meaningful connections.
- **Content Creation**
  Generate content ideas or write articles based on the professional experiences and skills of LinkedIn users.
- **Sales Outreach**
  Personalize sales pitches by understanding the background and interests of potential clients or partners.

## Built With

* Frontend: React + Vite + TailwindCSS
* Backend: FastAPI + Python

## Getting Started

> Refer to [LOCALHOST.md](LOCALHOST.md) for a more detailed installation guide for non-technical users.

### Prerequisites

* python 3.12
* pip
* npm (optional, for building the frontend)
* A valid LinkedIn account (don't use your own if possible)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/endernoke/linkedingest.git
   cd linkedingest
   ```

2. Create a `.env` file in the project's root directory and add the following environment variables:
   ```env
   LINKEDIN_AGENT_USERNAME=your_linkedin_email
   LINKEDIN_AGENT_PASSWORD=your_linkedin_password
   
   VITE_APP_NAME=LinkedIngest
   VITE_APP_DESCRIPTION=Transform LinkedIn profiles into prompt-ready data
   ```
   This LinkedIn account will be interacting with LinkedIn's API when fetching user data. Use a secondary account if possible, as it might get restricted/banned by LinkedIn. Though this has never happened with anti rate-limiting turned on during testing.


3. Install dependencies
  Install necessary dependencies in a Python virtual environment (optional if you know what you're doing).
  - For Mac/Linux:
   ```sh
   python3 -m venv venv
   source ./venv/bin/activate
   pip install -r backend/requirements.txt
   ```
  - For Windows:
   ```sh
   python -m venv venv
   .\venv\scripts\activate
   pip install -r backend\requirements.txt
   ```

4. Build the Frontend
  - Option 1: Build from source (recommended)
    ```
    cd frontend
    npm install
    npm run build
    cd ..
    ```
  - Option 2: Get dist files from releases page
    If you don't want to build the frontend distribution yourself, you can download them directly from the releases page. Note that these distribution files may not be the most up-to-date version.
    1. Download and extract the `distribution-files` archive from the latest release
    2. Inside the extracted archive, there is a `dist` folder. Move it inside the `frontend` directory

5. Start the application
   ```sh
   cd backend
   uvicorn app.main:app --host 0.0.0.0 --port 10000
   ```

6. The app will be running on `http://localhost:10000`. Navigate to this link in your browser to use the webapp.

## Project Configurations

This project intentionally implemented cooldowns between requests and "noise" requests when interacting with LinkedIn's API in order to prevent your account from being rate-limited/restricted. For better performance, you might want to tweak the behavior when fetching LinkedIn profiles.

You can override the default configurations in `backend/config.yaml`.
```
anti_rate_limiting:
  delay: off  # Disable delay between requests
  noise: off  # Disable making random requests
```
Change these configurations at your own risk.

## API Endpoints

> If  you are a developer who want to fetch LinkedIn profile ingests, I strongly recommend you host LinkedIngest locally instead of directly hitting endpoints in the demo website. Loading time in the demo website can often take more than 20 seconds, but you can optimize it to less than 4 seconds with anti rate-limiting turned off when hosting locally.

The main API endpoint of LinkedIngest is `/api/profile/<profile-id>`. The response structure is as follows:
```
{
  "full_name": "string",
  "summary": "formatted string",
  "experience": "formatted string",
  "education": "formatted string",
  "honors": "formatted string",
  "certifications": "formatted string",
  "projects": "formatted string",
  "publications": "formatted string",
  "volunteer": "formatted string",
  "skills": "formatted string",
  "languages": "formatted string",
  "posts: "formatted string",
  "raw": {
    "profile": {...}, // raw user profile data from LinkedIn's internal API
    "posts": [...] // list of raw user posts data from LinkedIn's internal API
  }
}
```
The absence of a profile section is indicated by an empty string. The `raw.posts` property may be `null` if posts data fail to be fetched.


## Contributing

Any contributions you make are **greatly appreciated**. Please:

1. Open an issue describing what you will be working on (bug report / feature request)
2. Fork the Project
3. Create your Feature Branch and make your changes
4. Open a Pull Request

You can also contribute by:
- [Reporting Bugs](https://github.com/endernoke/linkedingest/issues/new?template=bug_report.md)
- [Requesting Features](https://github.com/endernoke/linkedingest/issues/new?template=feature_request.md)

## License

Distributed under the [MIT License](LICENSE).

## Credits

Author: [James Zheng](https://linkedin.com/in/james-zheng-zi)
Project Link: [https://github.com/endernoke/linkedingest](https://github.com/endernoke/linkedingest)

* [linkedin-api](https://github.com/tomquirk/linkedin-api) - Python library for accessing LinkedIn data
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template) - README template used for this project
