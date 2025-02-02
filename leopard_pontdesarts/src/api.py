from fastapi import FastAPI, HTTPException
from src.tasks import get_leopard_task
from crewai import Crew
import json
import requests
import logging
import yaml
import os
from dotenv import load_dotenv

# ✅ Load .env for local development
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ✅ Load configuration from environment variables or YAML file
CONFIG_FILE_PATH = os.getenv("CONFIG_FILE", "/app/configs/config.yaml")  # Default in container

config = {}
if os.path.exists(CONFIG_FILE_PATH):
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config = yaml.safe_load(file) or {}
    except Exception as e:
        logger.error(f"❌ Error loading config file: {e}")

# ✅ Function to load values from ENV with fallback to config.yaml
def get_config_value(key_path: str, env_var: str, default=None):
    """Retrieve config value from ENV or YAML with default fallback."""
    env_value = os.getenv(env_var)
    if env_value:
        return env_value

    keys = key_path.split(".")
    temp_config = config
    for key in keys:
        if isinstance(temp_config, dict):
            temp_config = temp_config.get(key, None)
        else:
            return default  # Return default if path is invalid

    return temp_config if temp_config is not None else default

# ✅ Load API and Formatter URLs
LLM_API_KEY = get_config_value("llm.api_key", "LLM_API_KEY")
LLM_MODEL_NAME = get_config_value("llm.model_name", "LLM_MODEL", "deepseek-r1-distill-qwen-14b")
LLM_BASE_URL = get_config_value("llm.base_url", "LLM_BASE_URL")
FORMATTER_URL = get_config_value("formatter.api_url", "FORMATTER_API_URL", "http://localhost:8001/process")

# ✅ Debug Logs
logger.info(f"🔍 Loaded LLM_BASE_URL: {LLM_BASE_URL}")
logger.info(f"🔍 Loaded LLM_API_KEY: {LLM_API_KEY}")

@app.get("/")
def home():
    return {"message": "Leopard Pont des Arts API is running!"}

@app.get("/leopard-crossing")
def leopard_crossing():
    """Default endpoint: Returns raw agent response."""
    return execute_leopard_task()

@app.get("/leopard-crossing-ui")
def leopard_crossing_ui():
    """Returns agent response formatted for UI using the external formatter."""
    raw_result = execute_leopard_task()
    return call_formatter(raw_result)

def execute_leopard_task():
    """Runs the agent and returns computed response."""
    if not LLM_BASE_URL or not LLM_API_KEY:
        return {"error": "Missing LLM API URL or API key in config"}

    task = get_leopard_task()
    crew = Crew(agents=[task.agent], tasks=[task], verbose=True)
    result = crew.kickoff()

    try:
        return json.loads(result.raw) if hasattr(result, "raw") else {"error": "Unexpected response"}
    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON response from Crew")
        return {"error": "Invalid JSON response"}

# ✅ Ensure `app` is available when running `uvicorn src.api:app`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
