from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
import logging
import uuid
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Menstrual Health AI Advisor",
    description="AI-powered menstrual health advisor with Knowledge Graph",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="deployment/static"), name="static")
templates = Jinja2Templates(directory="deployment/templates")

# Initialize your ML system
from menstrual_system import WebMenstrualSystem
ml_system = WebMenstrualSystem()
system_loaded = False

# Simple in-memory storage for demo
analyses_db = []

@app.on_event("startup")
async def startup_event():
    """Initialize the ML system on startup"""
    global system_loaded
    try:
        logger.info("🔄 Loading Menstrual Health System...")
        system_loaded = ml_system.load()
        if system_loaded:
            logger.info("✅ System loaded successfully!")
        else:
            logger.error("❌ Failed to load system")
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        system_loaded = False

# Basic routes
@app.get("/")
async def root():
    return {
        "message": "Menstrual Health AI API", 
        "status": "running", 
        "ml_loaded": system_loaded,
        "system": "Knowledge Graph + Rule-based Predictor"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(), 
        "ml_system": "loaded" if system_loaded else "loading"
    }

# HTML routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "ml_loaded": system_loaded
    })

@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    return templates.TemplateResponse("analysis.html", {
        "request": request,
        "ml_loaded": system_loaded
    })

# API routes
@app.post("/api/analyze")
async def analyze_health_data(
    phase: str = Form(...),
    pain_level: int = Form(...),
    flow_intensity: str = Form("moderate"),
    mood: str = Form("N/A"),
    sleep_hours: float = Form(7.0),
    fatigue: str = Form("Medium"),
    headaches: str = Form("Medium"),
    bloating: str = Form("Medium"),
    day_in_cycle: int = Form(15),
    age: int = Form(25),
    contraception_type: str = Form("None")
):
    """Analyze health data using the system"""
    if not system_loaded:
        return {
            "success": False,
            "error": "System still loading. Please try again in a moment."
        }
    
    try:
        # Prepare user data
        user_data = {
            'age': age,
            'phase': phase,
            'pain_nrs': pain_level,
            'flow_intensity': flow_intensity,
            'contraception_type': contraception_type,
            'mood': mood,
            'sleep_hours': sleep_hours,
            'fatigue': fatigue,
            'headaches': headaches,
            'bloating': bloating,
            'day_in_cycle': day_in_cycle
        }
        
        # Use the system for analysis
        results = ml_system.analyze(user_data)
        
        if 'error' in results:
            return {
                "success": False,
                "error": results['error']
            }
        
        # Store analysis
        analysis_id = str(uuid.uuid4())[:8]
        analyses_db.append({
            "id": analysis_id,
            "user_data": user_data,
            "analysis": results,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 20 analyses
        if len(analyses_db) > 20:
            analyses_db.pop(0)
        
        return {
            "success": True,
            "analysis": results,
            "analysis_id": analysis_id,
            "timestamp": datetime.now().isoformat(),
            "ml_system_used": True,
            "llm_used": results.get('llm_used', False)
        }
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return {
            "success": False,
            "error": "Analysis failed",
            "detail": str(e)
        }

@app.get("/api/analysis/history")
async def get_analysis_history():
    """Get analysis history"""
    return {
        "success": True, 
        "history": analyses_db[-10:] if analyses_db else [],
        "total_analyses": len(analyses_db)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
