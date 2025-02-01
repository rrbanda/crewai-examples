from fastapi import FastAPI
from src.tasks import get_leopard_task
from crewai import Crew
import json

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Leopard Pont des Arts API is running!"}

@app.get("/leopard-crossing")  # ✅ Renamed for clarity
def leopard_crossing_time():
    """Trigger the agent to compute crossing time."""
    task = get_leopard_task()
    crew = Crew(agents=[task.agent], tasks=[task], verbose=True)

    result = crew.kickoff()

    try:
        final_result = json.loads(result.raw) if hasattr(result, "raw") else {"error": "Unexpected response"}
    except json.JSONDecodeError:
        final_result = {"error": "Invalid JSON response"}

    return final_result
