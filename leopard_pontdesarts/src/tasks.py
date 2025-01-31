from crewai import Task
from src.agents import LeopardPontDesArtsAgent
import os

# Fetch API details
llm_url = os.getenv("LLM_API_URL", "http://localhost:11434")
llm_model = os.getenv("LLM_MODEL", "mistral")
api_key = os.getenv("LLM_API_KEY")

def get_leopard_task():
    return Task(
        description="How many seconds would it take for a leopard at full speed to run through Pont des Arts?",
        expected_output="Approximate time in seconds + brief reasoning",
        agent=LeopardPontDesArtsAgent(model=llm_model, llm_url=llm_url, api_key=api_key)
    )
