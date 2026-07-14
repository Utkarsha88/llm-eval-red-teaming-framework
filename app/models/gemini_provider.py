from google import genai
from google.genai import types
from app.models.base_llm import BaseLLM
from app.utils.config import settings
from app.utils.logger import logger

class GeminiProvider(BaseLLM):
    """
    Concrete implementation for Google Gemini models.
    Utilizes the modern google-genai unified SDK.
    """
    
    def __init__(self, model_name: str):
        super().__init__(model_name=model_name)
        
        if not settings.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is missing from environment configurations.")
            raise ValueError("Gemini API key must be provided.")
            
        # Initialize the native asynchronous client (.aio)
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY).aio

    async def generate(self, prompt: str, temperature: float = 0.0, max_tokens: int = 1000) -> str:
        try:
            logger.info(f"Sending request to Gemini model: {self.model_name}")
            
            # Map our universal parameters to Gemini's specific configuration object
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            response = await self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config
            )
            
            if not response.text:
                logger.warning(f"Received empty response from {self.model_name}")
                return ""
                
            return response.text
            
        except Exception as e:
            logger.error(f"Generation failed for model {self.model_name}: {str(e)}")
            return f"ERROR: Generation failed due to provider exception: {str(e)}"