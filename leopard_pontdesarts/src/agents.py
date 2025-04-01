import yaml
import logging
from pydantic import Field
from crewai import Agent
from src.llm import CustomLLM

# ✅ Load Agent & Prompt Configurations
try:
    with open("configs/agents.yaml", "r") as file:
        agent_configs = yaml.safe_load(file) or {}
    with open("configs/prompts.yaml", "r") as file:
        prompt_configs = yaml.safe_load(file) or {}
except FileNotFoundError as e:
    logging.error(f"❌ Config file not found: {e}")
    agent_configs, prompt_configs = {}, {}

logger = logging.getLogger(__name__)

class LeopardPontDesArtsAgent(Agent):
    role: str = Field(default=agent_configs.get("leopard_pont_des_arts_agent", {}).get("role", "AI Researcher"))
    goal: str = Field(default=agent_configs.get("leopard_pont_des_arts_agent", {}).get("goal", "Provide insights about leopards."))
    backstory: str = Field(default=agent_configs.get("leopard_pont_des_arts_agent", {}).get("backstory", "A specialist in wildlife biology."))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._llm = CustomLLM()
        logger.info(f"✅ Initialized Agent: {self.role} using {self._llm.model_name}")

    def execute_task(self, task, context=None, tools=None):
        """Run prompt directly through LLM without external search."""
        prompt = prompt_configs.get("leopard_pont_des_arts_prompt", "❌ Missing prompt in config!")
        logger.info(f"🚀 Sending prompt to LLM: {prompt}")
        return self._llm.infer(prompt)
