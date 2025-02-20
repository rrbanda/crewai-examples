import requests
import json
import logging
import os
import re
from time import sleep
from datetime import datetime

logger = logging.getLogger(__name__)

class CustomLLM:
    def __init__(self):
        """Load LLM Configuration Dynamically from OpenShift ConfigMap"""
        
        # Get the active LLM provider from the ConfigMap
        self.provider = os.getenv("ACTIVE_LLM", "vllm").lower()

        # Dynamically load model and base URL based on the active LLM
        self.base_url = os.getenv(f"{self.provider.upper()}_BASE_URL", "").strip().strip('"').rstrip("/")
        self.model_name = os.getenv(f"{self.provider.upper()}_MODEL", "default-model")
        self.api_key = os.getenv("LLM_API_KEY", None)  # Some providers require API keys

        self.max_retries = 3

        # ✅ Fix for Podman localhost issue
        if self.base_url == "http://localhost:8000":
            self.base_url = "http://host.containers.internal:8000"

        logger.info(f"✅ Using LLM Provider: {self.provider} | Model: {self.model_name} | URL: {self.base_url}")

        if not self.base_url:
            logger.error("❌ LLM Base URL is missing. Check ConfigMap or environment variables.")
        if not self.api_key and self.provider in ["openai", "granite"]:
            logger.warning("⚠️ No LLM API Key provided. Some endpoints may require authentication.")

    def infer(self, prompt: str) -> str:
        """Send a prompt to the selected LLM API and return JSON response."""
        if not self.base_url:
            logger.error("❌ No LLM API URL configured.")
            return json.dumps({"error": "Missing LLM API URL in config"})

        # ✅ API payloads for different LLMs
        if self.provider == "vllm":
            url = f"{self.base_url}/v1/completions"
            payload = {"model": self.model_name, "prompt": prompt, "temperature": 0.1, "max_tokens": 1000}
        elif self.provider == "ollama":
            url = f"{self.base_url}/api/generate"
            payload = {"model": self.model_name, "prompt": prompt}
        elif self.provider == "granite":
            url = f"{self.base_url}/models/{self.model_name}:generateContent"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
        else:  # Default OpenAI-compatible API
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

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=120)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ LLM API Error on attempt {attempt}: {e}")
                if attempt < self.max_retries:
                    sleep(5)
                else:
                    return json.dumps({"error": "LLM API request failed after retries"})
