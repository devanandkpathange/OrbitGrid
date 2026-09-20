"""
GridPoint — Optimization & Maps Backend (FastAPI Application)
Role 3: Mathematical Optimization & Geographic Intelligence Engine for India
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.optimize import router as optimize_router
from .api.benchmark import router as benchmark_router
from .api.elbow import router as elbow_router
from .api.hubs import router as hubs_router
from .api.demo import router as demo_router
from .api.search import router as search_router
from .api.documents import router as documents_router
from .api.feasibility import router as feasibility_router
from .api.copilot import router as copilot_router
from .api.auth import router as auth_router
from .core.config import settings
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="GridPoint — Warehouse Location Optimization Engine",
    description=(
        "Computational core for warehouse location optimization across India. "
        "Solves capacitated facility location (CFLP), calculates logistics freight in INR (₹), "
        "evaluates Pareto elbow curves, and outputs GeoJSON catchment boundaries for Leaflet."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend integration (React / Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any local frontend development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(optimize_router)
app.include_router(benchmark_router)
app.include_router(elbow_router)
app.include_router(hubs_router)
app.include_router(demo_router)
app.include_router(search_router)
app.include_router(documents_router)
app.include_router(feasibility_router)
app.include_router(copilot_router)
app.include_router(auth_router)


class APIKeysPayload(BaseModel):
    google_maps_api_key: Optional[str] = None
    mapbox_access_token: Optional[str] = None
    openrouteservice_api_key: Optional[str] = None
    custom_llm_url: Optional[str] = None


@app.post("/api/config/keys", tags=["Configuration"])
async def update_api_keys(payload: APIKeysPayload):
    """
    Allows setting optional API keys and custom local LLM URL at runtime from the dashboard.
    """
    if payload.google_maps_api_key is not None:
        settings.GOOGLE_MAPS_API_KEY = payload.google_maps_api_key.strip() or None
    if payload.mapbox_access_token is not None:
        settings.MAPBOX_ACCESS_TOKEN = payload.mapbox_access_token.strip() or None
    if payload.openrouteservice_api_key is not None:
        settings.OPENROUTESERVICE_API_KEY = payload.openrouteservice_api_key.strip() or None
    if payload.custom_llm_url is not None:
        settings.CUSTOM_LLM_URL = payload.custom_llm_url.strip() or None

    return {
        "status": "updated",
        "google_maps_configured": bool(settings.GOOGLE_MAPS_API_KEY),
        "mapbox_configured": bool(settings.MAPBOX_ACCESS_TOKEN),
        "openrouteservice_configured": bool(settings.OPENROUTESERVICE_API_KEY),
        "custom_llm_configured": bool(settings.CUSTOM_LLM_URL),
        "custom_llm_url": settings.CUSTOM_LLM_URL
    }


@app.get("/api/config/keys", tags=["Configuration"])
async def get_api_keys_status():
    """
    Returns current configuration status of API keys (without leaking secrets).
    """
    return {
        "google_maps_configured": bool(settings.GOOGLE_MAPS_API_KEY),
        "mapbox_configured": bool(settings.MAPBOX_ACCESS_TOKEN),
        "openrouteservice_configured": bool(settings.OPENROUTESERVICE_API_KEY),
        "custom_llm_configured": bool(settings.CUSTOM_LLM_URL),
        "custom_llm_url": settings.CUSTOM_LLM_URL,
        "mode": "Custom LLM Connected" if settings.CUSTOM_LLM_URL else "100% Free Mode (₹0 cost)"
    }


import os
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

DASHBOARD_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates", "dashboard.html"))
PRESENTATION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates", "presentation.html"))

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    fav_file = os.path.join(STATIC_DIR, "gridpoint_logo.jpg")
    if os.path.exists(fav_file):
        return FileResponse(fav_file, media_type="image/jpeg")
    return HTMLResponse(content="", status_code=204)

@app.get("/", response_class=HTMLResponse, tags=["Dashboard"])
@app.get("/dashboard", response_class=HTMLResponse, tags=["Dashboard"])
async def get_dashboard():
    """
    GridPoint Interactive Dashboard view.
    """
    with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates", "script.html"))

@app.get("/presentation", response_class=HTMLResponse, tags=["Presentation"])
@app.get("/pitch", response_class=HTMLResponse, tags=["Presentation"])
async def get_presentation():
    """
    Orbit Grid Executive Pitch Deck Presentation View.
    """
    if os.path.exists(PRESENTATION_PATH):
        with open(PRESENTATION_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Presentation file not found</h1>", status_code=404)


@app.get("/script", response_class=HTMLResponse, tags=["Script"])
async def get_script():
    """
    Orbit Grid 2.5-Minute Demo Video Script View.
    """
    if os.path.exists(SCRIPT_PATH):
        with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Script file not found</h1>", status_code=404)


@app.get("/api/info", tags=["System"])
async def root_info():
    return {
        "system": "GridPoint Optimization & Maps Backend",
        "role": "Role 3 — Mathematical Optimization & Geographic Intelligence Engine",
        "target_region": "India",
        "currency": "INR (₹)",
        "status": "operational",
        "dashboard": "/",
        "documentation": "/docs"
    }


@app.get("/api/health", tags=["System"])
async def health():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "endpoints": [
            "POST /api/optimize",
            "POST /api/benchmark",
            "POST /api/elbow",
            "POST /api/feasibility",
            "POST /api/analyze-business",
            "POST /api/upload-document",
            "GET  /api/search",
            "GET  /api/hubs",
            "GET  /api/demo/{region}",
            "GET  /api/demo/sample-csvs",
            "GET  /api/demo/download/{filename}",
            "GET  /api/config/keys",
            "POST /api/config/keys"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
