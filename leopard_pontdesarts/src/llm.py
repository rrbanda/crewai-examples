import requests
import json
import yaml
import logging
import os
import re
from time import sleep
from datetime import datetime

logger = logging.getLogger(__name__)

# ✅ Load LLM Provider Config from YAML (if available)
CONFIG_FILE_PATH = "/app/configs/llm_provider_config.yaml"
config = {}

if os.path.exists(CONFIG_FILE_PATH):
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config = yaml.safe_load(file) or {}
    except FileNotFoundError as e:
        logger.error(f"❌ Config file not found: {e}")

# ✅ Function to Extract JSON Response from LLM Output
def extract_json(response_text):
    """Extract JSON from LLM response, handling markdown formatting."""
    match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        return match.group(1)  # Extract JSON block

    try:
        json_obj = json.loads(response_text)
        return json.dumps(json_obj, indent=2)
    except json.JSONDecodeError:
        logger.error("❌ LLM response is not valid JSON")
        return json.dumps({"error": "Invalid JSON received from LLM"})

class CustomLLM:
    def __init__(self):
        """Dynamically load LLM configuration from ENV variables or ConfigMap."""
        self.active_llm = os.getenv("ACTIVE_LLM", "openai")  # Default to OpenAI if not set
        self.llm_config = config.get("llms", {}).get(self.active_llm, {})

        # ✅ Load model-specific configurations
        self.base_url = os.getenv(f"{self.active_llm.upper()}_BASE_URL", self.llm_config.get("base_url", "")).strip().strip('"').rstrip("/")
        self.model_name = os.getenv(f"{self.active_llm.upper()}_MODEL", self.llm_config.get("model_name", "default-model"))
        self.api_key = os.getenv(f"{self.active_llm.upper()}_API_KEY", self.llm_config.get("api_key", None))
        self.max_retries = 3

        # ✅ Fix for Podman localhost issue
        if self.base_url == "http://localhost:8000":
            self.base_url = "http://host.containers.internal:8000"

        logger.info(f"✅ Using LLM Provider: {self.active_llm} | Model: {self.model_name} | URL: {self.base_url}")

        if not self.base_url:
            logger.error("❌ LLM Base URL is missing. Check ConfigMap or .env file")
        if not self.api_key and self.active_llm not in ["mistral", "ollama", "vllm"]:
            logger.warning("⚠️ No LLM API Key provided. Some endpoints may require authentication.")

    def infer(self, prompt: str) -> str:
        """Send a prompt to the selected LLM API and return JSON response."""
        if not self.base_url:
            logger.error("❌ No LLM API URL configured.")
            return json.dumps({"error": "Missing LLM API URL in config"})

        # ✅ Detect provider and format request accordingly
        if self.active_llm == "vllm":
            url = f"{self.base_url}/v1/completions"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "temperature": 0.1,
                "max_tokens": 1000,
            }
        elif self.active_llm == "ollama":
            url = f"{self.base_url}/api/generate"
            payload = {"model": self.model_name, "prompt": prompt}
        elif self.active_llm == "gemini":
            url = f"{self.base_url}/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
        else:  # Default to OpenAI API format
            url = f"{self.base_url}/v1/chat/completions"
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "Respond in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.1,
            }

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"} if self.api_key else {}

        for attempt in range(1, self.max_retries + 1):
            try:
                start_time = datetime.now()
                response = requests.post(url, json=payload, headers=headers, timeout=120)
                response.raise_for_status()
                data = response.json()
                elapsed_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"⏱️ LLM API Response Time: {elapsed_time:.2f} seconds")

                # ✅ Parse response correctly
                if self.active_llm == "vllm":
                    return json.dumps({"text": data["choices"][0]["text"].strip()}, indent=2)

                choices = data.get("choices", [])
                if choices:
                    response_text = choices[0].get("message", {}).get("content", "").strip()
                    json_part = extract_json(response_text)
                    return json.dumps(json.loads(json_part), indent=2) if json_part else json.dumps({"error": "Invalid JSON received from LLM"})

                return json.dumps({"error": "Empty response from LLM"})

            except requests.exceptions.RequestException as e:
                logger.error(f"❌ LLM API Error on attempt {attempt}: {e}")
                if attempt < self.max_retries:
                    sleep(5)
                    logger.info(f"🔄 Retrying... Attempt {attempt + 1}/{self.max_retries}")
                else:
                    return json.dumps({"error": "LLM API request failed after retries"})
