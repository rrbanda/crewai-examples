import requests
import json
import logging
import os
import re
from time import sleep
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Ensure logs are visible

class CustomLLM:
    def __init__(self):
        """Load provider and model configuration dynamically from OpenShift ConfigMap & Secret"""

        # Get Active Provider from ConfigMap (example: "ollama", "vllm", "granite", "openai", etc.)
        self.provider = os.getenv("ACTIVE_PROVIDER", "default").lower()

        # Get corresponding model for the provider
        self.model_name = os.getenv(f"{self.provider.upper()}_MODEL", "default-model").strip()
        self.base_url = os.getenv(f"{self.provider.upper()}_BASE_URL", "").strip()
        self.api_key = os.getenv("LLM_API_KEY", None)  # API Key (only for certain providers)

        # ✅ Debugging logs to verify the loaded configuration
        logger.info(f"🔍 ACTIVE PROVIDER: {self.provider}")
        logger.info(f"🔍 MODEL: {self.model_name}")
        logger.info(f"🔍 BASE URL: {self.base_url or 'MISSING'}")
        logger.info(f"🔍 API KEY: {'SET' if self.api_key else 'NOT SET'}")

        # Error handling for missing base URL
        if not self.base_url:
            logger.error("❌ Base URL is missing. Check ConfigMap or environment variables.")
    
    def infer(self, prompt: str) -> str:
        """Send a prompt to the selected LLM API and return JSON response."""
        if not self.base_url:
            logger.error("❌ No API URL configured.")
            return json.dumps({"error": "Missing API URL in config"})

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # 🛠 API-Specific Request Format Handling
        if self.provider == "vllm":
            url = f"{self.base_url}/v1/completions"
            payload = {"model": self.model_name, "prompt": prompt, "temperature": 0.1, "max_tokens": 1000}
        elif self.provider == "ollama":
            url = f"{self.base_url}/api/generate"
            payload = {"model": self.model_name, "prompt": prompt}
        elif self.provider == "gemini":
            url = f"{self.base_url}/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
        elif self.provider == "deepseek":
            url = f"{self.base_url}/v1/chat/completions"
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500,
            }
        else:  # Default to OpenAI-compatible models
            url = f"{self.base_url}/v1/chat/completions"
            payload = {
                "model": self.model_name,
                "messages": [{"role": "system", "content": "Respond in JSON format only."}, {"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.1,
            }

        # 🔄 Retry mechanism
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                start_time = datetime.now()
                response = requests.post(url, json=payload, headers=headers, timeout=120)
                response.raise_for_status()
                data = response.json()

                elapsed_time = (datetime.now() - start_time).total_seconds()
                logger.info(f"⏱️ API Response Time: {elapsed_time:.2f} seconds")
                logger.info(f"✅ Raw API Response: {json.dumps(data, indent=2)}")

                # ✅ Extract relevant response text
                if self.provider == "vllm":
                    return json.dumps({"text": data["choices"][0]["text"].strip()}, indent=2)

                choices = data.get("choices", [])
                if choices:
                    response_text = choices[0].get("message", {}).get("content", "").strip()
                    return json.dumps({"response": response_text}, indent=2)

                return json.dumps({"error": "Empty response from LLM"})

            except requests.exceptions.RequestException as e:
                logger.error(f"❌ API Error on attempt {attempt}: {e}")
                if attempt < max_retries:
                    sleep(5)
                    logger.info(f"🔄 Retrying... Attempt {attempt + 1}/{max_retries}")
                else:
                    return json.dumps({"error": "API request failed after retries"})
