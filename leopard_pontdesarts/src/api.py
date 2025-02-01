from fastapi import FastAPI, HTTPException
from src.tasks import get_leopard_task
from crewai import Crew
import json
import requests
import logging
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ✅ Load configuration from config.yaml
try:
    with open("configs/config.yaml", "r") as file:
        config = yaml.safe_load(file) or {}
except FileNotFoundError as e:
    logger.error(f"❌ Config file not found: {e}")
    config = {}

# ✅ Dynamically load formatter service URL from config.yaml
FORMATTER_URL = config.get("formatter", {}).get("api_url", "http://localhost:8001/process")  # Default if missing

@app.get("/")
def home():
    return {"message": "Leopard Pont des Arts API is running!"}

def call_formatter(data):
    """Send the response to the external formatter service with the correct structure."""
    payload = {
        "format": "json",
        "data": data
    }
    try:
        response = requests.post(FORMATTER_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        response.raise_for_status()
        return response.json()  # ✅ Returns formatted response
    except requests.exceptions.HTTPError as e:
        logger.error(f"❌ Formatter service error: {e.response.status_code} {e.response.text}")
        return {"error": f"Formatter failed with status {e.response.status_code}", "details": e.response.text}
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Formatter service error: {e}")
        return data  # Return original response if formatter fails

def execute_leopard_task():
    """Runs the agent and returns the computed response."""
    task = get_leopard_task()
    crew = Crew(agents=[task.agent], tasks=[task], verbose=True)

    result = crew.kickoff()

    try:
        return json.loads(result.raw) if hasattr(result, "raw") else {"error": "Unexpected response"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}

@app.get("/leopard-crossing")
def leopard_crossing():
    """Default endpoint: Returns raw agent response."""
    return execute_leopard_task()

@app.get("/leopard-crossing-ui")
def leopard_crossing_ui():
    """Returns agent response formatted for UI using the external formatter."""
    raw_result = execute_leopard_task()
    return call_formatter(raw_result)
