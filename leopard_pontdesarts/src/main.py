import logging
import json
from crewai import Crew
from src.tasks import get_leopard_task

logging.basicConfig(level=logging.INFO)

task = get_leopard_task()
crew = Crew(agents=[task.agent], tasks=[task], verbose=True)

if __name__ == "__main__":
    result = crew.kickoff()
    try:
        final_result = json.dumps(json.loads(result.raw), indent=2) if hasattr(result, "raw") else result.raw
    except json.JSONDecodeError:
        final_result = result.raw
    print("\n=== FINAL CREW RESULT ===")
    print(final_result)
