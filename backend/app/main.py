from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .api.linkedin import LinkedInAgent
from .models.profile import ProfileResponse

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static assets
app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"), name="assets")

@app.get("/")
async def read_root():
    return FileResponse("../frontend/dist/index.html")

@app.get("/in/{profile_id}")
async def profile_page(profile_id: str):
    # Serve the same index.html - frontend will handle routing
    return FileResponse("../frontend/dist/index.html")

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
