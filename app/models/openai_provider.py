from openai import AsyncOpenAI
from app.models.base_llm import BaseLLM
from app.utils.config import settings
from app.utils.logger import logger

class OpenRouterProvider(BaseLLM):
    """
    Concrete implementation for models accessed via OpenRouter.
    Utilizes OpenAI-compatible routing client architecture.
    """
    
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name)
        
        if not settings.OPENROUTER_API_KEY:
            logger.error("OPENROUTER_API_KEY is missing from environment configurations.")
            raise ValueError("OpenRouter API key must be provided.")
            
        # OpenRouter uses the OpenAI client but points to a different Base URL
        self.client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": "https://github.com/sentinel-llm", 
                "X-Title": "SentinelLLM Framework",
            }
        )

    async def generate(self, prompt: str, temperature: float = 0.0, max_tokens: int = 1000) -> str:
        try:
            logger.info(f"Sending request to OpenRouter model: {self.model_name}")
            
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            if not response.choices:
                logger.warning(f"Received empty completion choices from {self.model_name}")
                return ""
                
            return response.choices[0].message.content or ""
            
        except Exception as e:
            logger.error(f"Generation failed for model {self.model_name}: {str(e)}")
            # RAISE the exception so the Runner knows the API call actually failed!
            raise e