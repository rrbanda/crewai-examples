import logging
import json
from crewai import Crew
from src.tasks import get_leopard_task

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Create Crew and Run Task
leopard_task = get_leopard_task()

crew = Crew(
    agents=[leopard_task.agent],
    tasks=[leopard_task],
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()

    # Extract response correctly
    response_text = result.raw if hasattr(result, "raw") else json.dumps({"error": "Unexpected response type"}, indent=2)

    try:
        json_output = json.loads(response_text)
        final_result = json.dumps(json_output, indent=2)
    except json.JSONDecodeError:
        final_result = response_text  # Print raw text if not JSON

    print("\n=== FINAL CREW RESULT ===")
    print(final_result)
