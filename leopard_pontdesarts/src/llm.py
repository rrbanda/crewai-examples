import requests
import json
import logging
import os
import re
from time import sleep
from typing import Optional

# Setup logging
logger = logging.getLogger(__name__)

# Extract JSON from mixed text response
def extract_json(response_text):
    """Extracts the JSON part from the LLM response."""
    match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        return match.group(1)  # Extract only the JSON part
    return None  # Return None if no JSON is found

class CustomLLM:
    def __init__(self, model: str, base_url: str, api_key: Optional[str] = None):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.max_retries = 3
        logger.info(f"Initialized LLM with model: {self.model}, URL: {self.base_url}")

    def infer(self, prompt: str) -> str:
        """Send a prompt to the LLM API and return a valid JSON response as a string."""
        logger.info(f"Sending request to LLM ({self.base_url}) with model '{self.model}'.")

        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        } if self.api_key else {}

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Return only JSON output. No explanations."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.1,
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=120)
                response.raise_for_status()
                data = response.json()

                logger.info(f"Raw LLM API Response: {json.dumps(data, indent=2)}")

                choices = data.get("choices", [])
                response_text = choices[0].get("message", {}).get("content", "").strip() if choices else ""

                if not response_text:
                    return json.dumps({"error": "Empty response from LLM"})

                json_part = extract_json(response_text)
                if json_part:
                    return json.dumps(json.loads(json_part), indent=2)  # Return properly formatted JSON
                else:
                    return json.dumps({"error": "Invalid JSON received from LLM"})

            except requests.exceptions.RequestException as e:
                logger.error(f"[CustomLLM] Error on attempt {attempt}: {e}")

                if attempt < self.max_retries:
                    sleep(5)
                    logger.info(f"Retrying... Attempt {attempt + 1}/{self.max_retries}")
                else:
                    return json.dumps({"error": "LLM API request failed after retries"})
