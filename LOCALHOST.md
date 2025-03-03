# Running LinkedIngest Locally

This guide will help you set up and run LinkedIngest on your computer.

Time required: 10-15 minutes, depending on your familiarity with Python and command-line interface.

> **Note:** The following instructions are intended for non-technical users. If you are familiar with programming tools, refer to the Getting Started section in [README.md](README.md).

## Prerequisites

Before starting, make sure you have Python **3.12** (not latest version) installed:
Download and install from [python.org](https://www.python.org/downloads/)
   > During installation, make sure to check "Add Python to PATH"

You'll also need:
- A LinkedIn account (preferably a secondary account)
- A text editor

## Installation

### 1. Download the Project
1. Go to [https://github.com/endernoke/linkedingest](https://github.com/endernoke/linkedingest)
2. Click the green "Code" button and click "Download ZIP"
3. Extract the ZIP file to a location on your computer

### 2. Set Up Configuration
1. Create a new file called `.env` in the extracted folder
2. Open `.env` with a text editor and add these lines:
   ```
   LINKEDIN_AGENT_USERNAME=your_linkedin_email
   LINKEDIN_AGENT_PASSWORD=your_linkedin_password
   ```
   Replace `your_linkedin_email` and `your_linkedin_password` with your actual LinkedIn credentials. This account will be interacting with LinkedIn's servers to  fetch users' data. Your credentials are only stored locally.
3. Save and close the file

### 3. Install Dependencies

#### For Windows:
1. Open Command Prompt and navigate to the extracted folder:
   ```sh
   cd path/to/linkedingest
   ```

2. Paste these commands into Command Prompt:
   ```sh
   python -m venv venv
   .\venv\scripts\activate
   pip install -r backend\requirements.txt
   ```

#### For Mac/Linux:
1. Open Terminal and navigate to the extracted folder:
   ```sh
   cd path/to/linkedingest
   ```
2. Paste these commands into the Terminal:
   ```sh
   python -m venv venv
   source ./venv/bin/activate
   python -m pip install -r backend/requirements.txt
   ```
   If you notice an error similar to "Command 'python' not found", try replacing `python` with `python3` in the above commands and run them again.

### 4. (Optional) Edit Project Configurations

This project intentionally implemented cooldowns between requests and "noise" requests when interacting with LinkedIn's servers in order to prevent your account from being rate-limited/restricted. For better performance, you might want to tweak the behavior when fetching LinkedIn profiles.

The project's configurations are stored in the file `path/to/linkedingest/backend/config.yaml`. Open this file with your text editor to edit the configurations.
```
anti_rate_limiting:
  delay: off  # Disable delay between requests
  noise: off  # Disable making random requests
```
Change these configurations at your own risk.

### 5. Start the Application

1. Make sure you're in the extracted folder
2. Run these commands:
   ```sh
   cd backend
   uvicorn app.main:app --host 0.0.0.0 --port 10000
   ```
3. If successful, you should see a bunch of output with this at the end:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
   ```
4. Go to `http://localhost:10000` in your browser. You should see LinkedIngest's homepage.

## Troubleshooting

### Common Issues:

1. **"Python is not recognized" error**
   Reinstall Python 3.12 with "Add Python to PATH" checked.

2. **Port 10000 is blocked by Firewall**
   Try to run the app on a different port (e.g. 8000) in Step 5:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   And go to the chosen port accordingly in your browser (e.g. `http://localhost:8000`)

3. **LinkedIn login fails**
   - Verify your LinkedIn credentials in the `.env` file
   - If you see something like `Login Challenge required` in the Command Prompt / Terminal, it means that LinkedIn is suspicious of your login attempt and threw you a security challenge. This project currently don't handle this. Your best bet is to login to LinkedIn on your browser and try again.

If you encounter any other problems, please Check our [Issues page](https://github.com/endernoke/linkedingest/issues). Create a new issue if none of them describes your problem.
