import yaml
import logging
from crewai import Task
from src.agents import LeopardPontDesArtsAgent

# Load Task Configs
try:
    with open("configs/tasks.yaml", "r") as file:
        task_configs = yaml.safe_load(file) or {}
except FileNotFoundError as e:
    logging.error(f"❌ Task config file not found: {e}")
    task_configs = {}

def get_leopard_task():
    return Task(
        description=task_configs["leopard_task"]["description"],
        expected_output=task_configs["leopard_task"]["expected_output"],
        agent=LeopardPontDesArtsAgent()
    )
