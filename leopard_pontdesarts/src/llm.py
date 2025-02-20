import requests
import json
import yaml
import logging
import os
import re
from time import sleep
from datetime import datetime

logger = logging.getLogger(__name__)

# ✅ Load LLM Provider Config from YAML if available
CONFIG_FILE_PATH = "configs/llm_provider_config.yaml"
config = {}

if os.path.exists(CONFIG_FILE_PATH):
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config = yaml.safe_load(file) or {}
    except Exception as e:
        logger.error(f"❌ Error loading config file: {e}")

# ✅ Extract JSON from response function
def extract_json(response_text):
    """Extract JSON part from LLM response (handles JSON inside markdown formatting)."""
    match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        return match.group(1)  # Extract JSON block

    # If model returns plain JSON without markdown formatting
    try:
        json_obj = json.loads(response_text)
        return json.dumps(json_obj, indent=2)
    except json.JSONDecodeError:
        logger.error("❌ LLM response is not valid JSON")
        return json.dumps({"error": "Invalid JSON received from LLM"})

class CustomLLM:
    def __init__(self):
        """Load LLM Configuration Dynamically"""
        self.provider = os.getenv("LLM_PROVIDER", "default")  # Auto-detect
        llm_config = config.get("llms", {}).get(self.provider, {})

        self.model_name = os.getenv("LLM_MODEL", llm_config.get("model_name", "default-model"))
        self.base_url = os.getenv("LLM_BASE_URL", llm_config.get("base_url", "")).strip().strip('"').rstrip("/")
        self.api_key = os.getenv("LLM_API_KEY")  # 🔥 OpenShift injects this securely
        self.max_retries = int(os.getenv("LLM_MAX_RETRIES", "3"))
        self.timeout = int(os.getenv("LLM_TIMEOUT", "120"))

        # 🔹 Fix for Podman (if running inside a container)
        if "localhost" in self.base_url and os.getenv("PODMAN_FIX", "False").lower() == "true":
            self.base_url = self.base_url.replace("localhost", "host.containers.internal")

        logger.info(f"✅ Using LLM Provider: {self.provider} | Model: {self.model_name} | URL: {self.base_url}")

        if not self.base_url:
            logger.error("❌ LLM Base URL is missing. Check OpenShift secrets or `.env`")
        if not self.api_key:
            logger.warning("⚠️ No LLM API Key detected. Ensure OpenShift secret is injected.")

    def infer(self, prompt: str) -> str:
        """Send a prompt to the selected LLM API and return JSON response."""
        if not self.base_url:
            return json.dumps({"error": "Missing LLM API URL in config"})

        url = f"{self.base_url}/v1/chat/completions"
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You must respond in JSON format."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.1,
        }

        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()

                logger.info(f"✅ LLM API Response: {json.dumps(data, indent=2)}")
                return json.dumps(data, indent=2)
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ LLM API Error on attempt {attempt}: {e}")
                if attempt < self.max_retries:
                    sleep(5)
                else:
                    return json.dumps({"error": "LLM API request failed after retries"})
