from app.models.base_llm import BaseLLM
from app.models.openai_provider import OpenRouterProvider
from app.models.gemini_provider import GeminiProvider
from app.utils.logger import logger

class LLMFactory:
    """
    Factory class to dynamically instantiate the correct LLM provider.
    """
    
    @staticmethod
    def create(model_name: str) -> BaseLLM:
        model_name_lower = model_name.lower()
        
        # If the string contains a "/", it is almost certainly an OpenRouter model
        # (e.g., "google/gemini-2.5-flash", "meta-llama/llama-3-8b-instruct")
        if "/" in model_name_lower:
            logger.info(f"Factory routing '{model_name}' to OpenRouterProvider.")
            return OpenRouterProvider(model_name=model_name)
            
        # If it's just "gemini-2.5-flash" (no prefix), route it to Google's native SDK
        elif "gemini" in model_name_lower:
            logger.info(f"Factory routing '{model_name}' to GeminiProvider.")
            return GeminiProvider(model_name=model_name)
            
        # Default fallback to OpenRouter
        else:
            logger.info(f"Factory routing '{model_name}' to OpenRouterProvider as fallback.")
            return OpenRouterProvider(model_name=model_name)