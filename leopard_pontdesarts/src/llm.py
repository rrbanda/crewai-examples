import requests
import json
import yaml
import logging
import os
import re
from time import sleep

logger = logging.getLogger(__name__)

# ✅ Load LLM Provider Config
CONFIG_FILE_PATH = "configs/llm_provider_config.yaml"
config = {}

if os.path.exists(CONFIG_FILE_PATH):
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config = yaml.safe_load(file) or {}
    except FileNotFoundError as e:
        logger.error(f"❌ Config file not found: {e}")

# ✅ Extract JSON helper function
def extract_json(response_text):
    """Extract JSON part from LLM response"""
    match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    return match.group(1) if match else None

class CustomLLM:
    def __init__(self):
        """Load LLM Configuration Dynamically"""
        provider = os.getenv("LLM_PROVIDER", "openai")  # Default to OpenAI
        llm_config = config.get("llms", {}).get(provider, {})

        self.model_name = os.getenv("LLM_MODEL", llm_config.get("model_name", "default-model"))
        self.base_url = os.getenv("LLM_BASE_URL", llm_config.get("base_url", "")).strip().strip('"').rstrip("/")
        self.api_key = os.getenv("LLM_API_KEY", llm_config.get("api_key", None))
        self.max_retries = 3

        logger.info(f"✅ Using LLM Provider: {provider} | Model: {self.model_name} | URL: {self.base_url}")

        if not self.base_url:
            logger.error("❌ LLM Base URL is missing. Check `.env` or `llm_provider_config.yaml`")
        if not self.api_key and provider not in ["mistral", "ollama"]:
            logger.warning("⚠️ No LLM API Key provided. Some endpoints may require authentication.")

    def infer(self, prompt: str) -> str:
        """Send a prompt to the selected LLM API and return JSON response."""
        if not self.base_url:
            logger.error("❌ No LLM API URL configured.")
            return json.dumps({"error": "Missing LLM API URL in config"})

        # ✅ Handle Special API Formats
        if "ollama" in self.base_url:
            url = f"{self.base_url}/api/generate"
            payload = {"model": self.model_name, "prompt": prompt}
        elif "gemini" in self.base_url:
            url = f"{self.base_url}/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
        else:
            url = f"{self.base_url}/v1/chat/completions"
            payload = {
                "model": self.model_name,
                "messages": [{"role": "system", "content": "Return only JSON output. No explanations."}, {"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.1,
            }

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"} if self.api_key else {}

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
