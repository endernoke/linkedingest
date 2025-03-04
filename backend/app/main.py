from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .admin.admin import setup_admin, authenticate_admin
from .api.linkedin import LinkedInAgent, FetchException, ParseException
from .api.linkedin import ChallengeException
from .models.profile import ProfileResponse
import os

app = FastAPI()

setup_admin()

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

try:
    linkedin_agent = LinkedInAgent()
except ChallengeException as e:
    print("LinkedIn login challenge required, you're screwed 💀")
    linkedin_agent = None
except Exception as e:
    print(f"Failed to initialize LinkedInAgent: {e}")
    linkedin_agent = None

@app.get("/api/profile/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: str):
    try:
        if linkedin_agent is None:
            raise HTTPException(status_code=400, detail="Service temporarily suspended.")
        profile_data = await linkedin_agent.get_ingest(profile_id)
        return profile_data
    except FetchException:
        raise HTTPException(status_code=400, detail="Failed to fetch profile")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    if linkedin_agent is None:
        raise HTTPException(
            status_code=503, 
            detail="Service temporarily suspended."
        )
    return {"status": "ok"}

@app.get("/api/queue")
async def waiting_count():
    if linkedin_agent is None:
        raise HTTPException(
            status_code=503, 
            detail="Service temporarily suspended."
        )
    return linkedin_agent.get_queue_status()

@app.post("/admin/refresh_agent")
async def refresh_agent(admin: bool = Depends(authenticate_admin)):
    """Endpoint to refresh the internal linkedin agent.  Requires admin authentication."""
    global linkedin_agent
    try:
        linkedin_agent = LinkedInAgent()  # Reinitialize
        return JSONResponse(content={"message": "LinkedIn agent refreshed successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing LinkedIn agent: {repr(e)}")

@app.post("/admin/suspend")
async def suspend_service(admin: bool = Depends(authenticate_admin)):
    """
    Endpoint to suspend API service. 
    Requires admin authentication.
    Post to /admin/refresh_agent to resume service.
    """
    global linkedin_agent
    try:
        linkedin_agent = None
        return JSONResponse(content={"message": "Service suspended successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error when attempting to suspend service: {repr(e)}")

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # 404 will be handled in frontend
    return FileResponse(os.path.join(root_dir, "frontend/dist/index.html"))
