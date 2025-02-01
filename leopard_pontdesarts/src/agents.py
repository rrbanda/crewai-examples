
import yaml
import logging
from pydantic import Field
from crewai import Agent
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from src.llm import CustomLLM

# Load Configs
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
    role: str = Field(default=agent_configs["leopard_pont_des_arts_agent"]["role"])
    goal: str = Field(default=agent_configs["leopard_pont_des_arts_agent"]["goal"])
    backstory: str = Field(default=agent_configs["leopard_pont_des_arts_agent"]["backstory"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ddg = DuckDuckGoSearchAPIWrapper()
        self._llm = CustomLLM()  # ✅ No need to pass URL or API key manually
        logger.info(f"✅ Initialized Agent: {self.role}")

    def execute_task(self, task, context=None, tools=None):
        prompt = prompt_configs.get("leopard_pont_des_arts_prompt", "❌ Missing prompt in config!")
        return self._llm.infer(prompt)
