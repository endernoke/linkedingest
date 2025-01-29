from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .api.linkedin import LinkedInAgent
from .models.profile import ProfileResponse
import os

app = FastAPI()

# root directory relative to the file is ../..
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
print(root_dir)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static assets
app.mount("/assets", StaticFiles(directory=os.path.join(root_dir, "frontend/dist/assets")), name="assets")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(root_dir, "frontend/dist/index.html"))

@app.get("/in/{profile_id:path}")
async def profile_page(profile_id: str):
    # Remove trailing slashes and anything after them
    clean_id = profile_id.split('/')[0]
    return FileResponse(os.path.join(root_dir, "frontend/dist/index.html"))

# Get favicon
@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(root_dir, "frontend/dist/favicon.ico"))

linkedin_agent = LinkedInAgent()

@app.get("/api/profile/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: str):
    try:
        profile_data = await linkedin_agent.get_ingest(profile_id)
        return profile_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # Handle 404 for undefined routes
    raise HTTPException(status_code=404, detail="Resource not found")
