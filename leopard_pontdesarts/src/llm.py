import requests
import json
import yaml
import logging
import re
from time import sleep
from typing import Optional

# Load Config File
try:
    with open("configs/config.yaml", "r") as file:
        config = yaml.safe_load(file) or {}
except FileNotFoundError as e:
    logging.error(f"❌ Config file not found: {e}")
    config = {}

logger = logging.getLogger(__name__)

def extract_json(response_text):
    """Extract JSON part from LLM response"""
    match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    return match.group(1) if match else None

class CustomLLM:
    def __init__(self):
        self.model = config.get("llm", {}).get("model", "default-model")
        self.base_url = config.get("llm", {}).get("api_url", "").rstrip("/")
        self.api_key = config.get("llm", {}).get("api_key", None)
        self.max_retries = 3
        logger.info(f"✅ Initialized LLM with model: {self.model}, URL: {self.base_url}")

    def infer(self, prompt: str) -> str:
        """Send a prompt to the LLM API and return JSON response."""
        if not self.base_url:
            logger.error("❌ No LLM API URL configured.")
            return json.dumps({"error": "Missing LLM API URL in config"})

        logger.info(f"📨 Sending request to LLM: {self.base_url} | Model: {self.model}")

        url = f"{self.base_url}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"} if self.api_key else {}

        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": "Return only JSON output. No explanations."}, {"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.1,
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=120)
                response.raise_for_status()
                data = response.json()

                logger.info(f"✅ Raw LLM API Response: {json.dumps(data, indent=2)}")

                choices = data.get("choices", [])
                response_text = choices[0].get("message", {}).get("content", "").strip() if choices else ""

                if not response_text:
                    return json.dumps({"error": "Empty response from LLM"})

                json_part = extract_json(response_text)
                return json.dumps(json.loads(json_part), indent=2) if json_part else json.dumps({"error": "Invalid JSON received from LLM"})

            except requests.exceptions.RequestException as e:
                logger.error(f"❌ LLM API Error on attempt {attempt}: {e}")
                if attempt < self.max_retries:
                    sleep(5)
                    logger.info(f"🔄 Retrying... Attempt {attempt + 1}/{self.max_retries}")
                else:
                    return json.dumps({"error": "LLM API request failed after retries"})
