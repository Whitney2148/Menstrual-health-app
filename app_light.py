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
    description="AI-powered menstrual health advisor",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="deployment/static"), name="static")
templates = Jinja2Templates(directory="deployment/templates")

# Simple in-memory storage
analyses_db = []

@app.get("/")
async def root():
    return {"message": "Menstrual Health AI API", "status": "running"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    return templates.TemplateResponse("analysis.html", {"request": request})

# Simple rule-based analysis for deployment
@app.post("/api/analyze")
async def analyze_health_data(
    phase: str = Form(...),
    pain_level: int = Form(...),
    flow_intensity: str = Form("moderate"),
    mood: str = Form("N/A"),
    sleep_hours: float = Form(7.0),
    day_in_cycle: int = Form(15)
):
    """Simple rule-based analysis for deployment"""
    try:
        # Simple rule-based recommendations
        symptoms = []
        if pain_level >= 3:
            symptoms.append('cramps')
        if pain_level >= 6:
            symptoms.append('severe_cramps')
        
        # Basic recommendations
        medications = ['ibuprofen', 'paracetamol'] if symptoms else []
        hygiene_products = ['pad', 'tampon']
        
        if flow_intensity == 'light':
            hygiene_products = ['pad', 'period_underwear']
        elif flow_intensity == 'heavy':
            hygiene_products = ['menstrual_cup', 'super_pad']
        
        # Calculate next period (simple rule)
        next_period_days = 28 - day_in_cycle if day_in_cycle <= 28 else 28
        
        results = {
            'advice': f"Based on your {phase} phase and symptoms, here are personalized recommendations.",
            'knowledge_graph_recommendations': {
                'medications': medications,
                'hygiene_products': hygiene_products,
                'lifestyle_tips': ['Stay hydrated', 'Get adequate sleep', 'Consider gentle exercise'],
                'symptoms_identified': symptoms
            },
            'predictions': {
                'next_period_in_days': next_period_days,
                'predicted_phase': phase
            },
            'llm_used': False,
            'kg_used': True
        }
        
        return {
            "success": True,
            "analysis": results,
            "analysis_id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": "Analysis failed",
            "detail": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
