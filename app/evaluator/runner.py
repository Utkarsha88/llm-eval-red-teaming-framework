import time
import asyncio
from typing import List
from app.models.base_llm import BaseLLM
from app.datasets.loader import EvaluationTestCase
from app.evaluator.result import EvaluationResult
from app.utils.logger import logger

class EvaluationRunner:
    """
    Coordinates the execution of datasets against a given LLM provider.
    """
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    async def evaluate_single(self, test_case: EvaluationTestCase) -> EvaluationResult:
        """Evaluates a single prompt and measures performance."""
        logger.info(f"Evaluating prompt ID: {test_case.id}")
        
        start_time = time.time()
        error_msg = None
        response_text = ""
        
        try:
            # Call the model via our universal factory interface
            response_text = await self.llm.generate(test_case.prompt)
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed on test case {test_case.id}: {error_msg}")
            
        latency = round(time.time() - start_time, 2)
        
        return EvaluationResult(
            test_case_id=test_case.id,
            category=test_case.category,
            prompt=test_case.prompt,
            expected_behavior=test_case.expected_behavior,
            model_name=self.llm.model_name,
            response=response_text,
            latency_seconds=latency,
            error=error_msg
        )

    async def run(self, dataset: List[EvaluationTestCase], concurrency_limit: int = 3) -> List[EvaluationResult]:
        """
        Executes a full dataset asynchronously using a semaphore for rate limiting.
        """
        logger.info(f"Starting evaluation run with {len(dataset)} test cases for {self.llm.model_name}")
        
        # The semaphore prevents us from overwhelming the API concurrently
        semaphore = asyncio.Semaphore(concurrency_limit)
        
        async def sem_task(test_case):
            async with semaphore:
                # Execute the prompt
                result = await self.evaluate_single(test_case)
                
                # THE FIX: Add a 2-second cooldown after every request 
                # so free-tier APIs (like OpenRouter) don't block us for spamming.
                await asyncio.sleep(2.0) 
                
                return result
                
        # Launch all tasks concurrently (but safely delayed)
        tasks = [sem_task(tc) for tc in dataset]
        results = await asyncio.gather(*tasks)
        
        logger.info(f"Completed evaluation run. Generated {len(results)} results.")
        return results

    