"""nutrition_agent package initialiser"""
from nutrition_agent.llm_client import NutritionLLMClient
from nutrition_agent.config import APP_NAME, APP_VERSION

__all__ = ["NutritionLLMClient", "APP_NAME", "APP_VERSION"]
