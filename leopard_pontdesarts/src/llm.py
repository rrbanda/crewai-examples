import requests
import json
import yaml
import logging
import os
import re
from time import sleep
from datetime import datetime

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = "configs/llm_provider_config.yaml"
config = {}

if os.path.exists(CONFIG_FILE_PATH):
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            config = yaml.safe_load(file) or {}
    except FileNotFoundError as e:
        logger.error(f"❌ Config file not found: {e}")

def extract_json(response_text):
    """Extract and parse the first valid JSON object from a messy response."""
    try:
        matches = re.findall(r'\{.*?\}', response_text, re.DOTALL)
        for match in matches:
            try:
                return json.dumps(json.loads(match.strip()), indent=2)
            except json.JSONDecodeError:
                continue
        raise ValueError("No valid JSON found")
    except Exception as e:
        logger.error(f"❌ Failed to extract JSON: {e}")
        return json.dumps({"error": "Invalid JSON received from LLM"})

class CustomLLM:
    def __init__(self):
        """Load config from ENV or YAML, with hardcoded cluster-safe fallbacks."""
        self.provider = os.getenv("ACTIVE_PROVIDER") or "vllm"
        llm_config = config.get("llms", {}).get(self.provider, {})

        # ✅ Hardcoded fallbacks for OpenShift cluster
        self.base_url = os.getenv(f"{self.provider.upper()}_BASE_URL") or llm_config.get("base_url") or \
            "https://healthcare-model-demo-kserve.apps.cluster-tcvkd.tcvkd.sandbox65.opentlc.com"
        self.model_name = os.getenv(f"{self.provider.upper()}_MODEL") or llm_config.get("model_name") or \
            "healthcare-model"
        self.api_key = os.getenv("LLM_API_KEY", llm_config.get("api_key", None))
        self.max_retries = 3

        # Fix for Podman/localhost usage
        if self.base_url == "http://localhost:8000":
            self.base_url = "http://host.containers.internal:8000"

        self.base_url = self.base_url.strip().rstrip("/")

        logger.info(f"✅ Using Provider: {self.provider} | Model: {self.model_name} | URL: {self.base_url}")
        if not self.base_url:
            logger.error("❌ LLM Base URL is missing.")
        if not self.api_key and self.provider not in ["mistral", "ollama", "vllm", "deepseek"]:
            logger.warning("⚠️ No API key provided for this provider.")

    def infer(self, prompt: str) -> str:
        """Send the prompt to the LLM and return structured JSON."""
        if not self.base_url:
            return json.dumps({"error": "Missing LLM API URL in config"})

        # 🔧 Construct API call depending on provider
        if self.provider == "vllm":
            url = f"{self.base_url}/v1/completions"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "temperature": 0.1,
                "max_tokens": 1000
            }
        elif self.provider == "ollama":
            url = f"{self.base_url}/api/generate"
            payload = {"model": self.model_name, "prompt": prompt}
        elif self.provider == "gemini":
            url = f"{self.base_url}/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
        elif self.provider == "deepseek":
            url = f"{self.base_url}/chat/completions"
            payload = {"model": self.model_name, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
        elif self.provider == "granite":
            url = f"{self.base_url}/v1/chat/completions"
            payload = {"model": self.model_name, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
        else:
            url = f"{self.base_url}/v1/chat/completions"
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "Respond in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
            }

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"} if self.api_key else {"Content-Type": "application/json"}

        for attempt in range(1, self.max_retries + 1):
            try:
                start = datetime.now()
                response = requests.post(url, json=payload, headers=headers, timeout=120)
                response.raise_for_status()
                data = response.json()

                elapsed = (datetime.now() - start).total_seconds()
                logger.info(f"⏱️ LLM API Response Time: {elapsed:.2f} seconds")
                logger.info(f"✅ Raw LLM API Response: {json.dumps(data, indent=2)}")

                if self.provider in ["vllm", "ollama"]:
                    raw = data["choices"][0].get("text", "").strip()
                    return extract_json(raw)

                choices = data.get("choices", [])
                if choices:
                    response_text = choices[0].get("message", {}).get("content", "").strip()
                    return extract_json(response_text)

                return json.dumps({"error": "Empty response from LLM"})

            except requests.exceptions.RequestException as e:
                logger.error(f"❌ API Error on attempt {attempt}: {e}")
                if attempt < self.max_retries:
                    logger.info(f"🔄 Retrying... Attempt {attempt + 1}/{self.max_retries}")
                    sleep(5)
                else:
                    return json.dumps({"error": "LLM API request failed after retries"})
