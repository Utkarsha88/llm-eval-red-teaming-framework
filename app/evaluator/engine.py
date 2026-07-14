import os
from typing import List, Dict, Any
from app.models.factory import LLMFactory
from app.datasets.loader import DatasetLoader
from app.evaluator.runner import EvaluationRunner
from app.evaluator.result import EvaluationResult
from app.redteam.metrics import HeuristicMetrics
from app.utils.logger import logger

class EvaluationEngine:
    """
    Orchestrates full evaluation execution loops across datasets and models.
    Combines raw processing with downstream diagnostic scoring.
    """

    def __init__(self):
        pass

    async def execute_run(
        self, 
        model_name: str, 
        dataset_path: str, 
        concurrency_limit: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Executes a targeted evaluation batch for a specific model against a dataset.
        
        Args:
            model_name (str): Identifier of the target evaluation model.
            dataset_path (str): Relative path to the targeting JSON asset.
            concurrency_limit (int): Semaphore capacity configuration.
            
        Returns:
            List[Dict[str, Any]]: Comprehensive processed payload including scores.
        """
        logger.info(f"Initializing Engine execution loop for model: {model_name} against {dataset_path}")
        
        # 1. Resolve and Load the Target Dataset
        test_cases = DatasetLoader.load(dataset_path)
        
        # 2. Resolve the Target Model via Factory Architecture
        model_instance = LLMFactory.create(model_name)
        
        # 3. Initialize the Runner Interface and Execute Network Calls Concurrently
        runner = EvaluationRunner(llm=model_instance)
        raw_results: List[EvaluationResult] = await runner.run(test_cases, concurrency_limit=concurrency_limit)
        
        # 4. Process and Grade Every Result Item
        scored_records = []
        for result in raw_results:
            logger.info(f"Grading response data for Test Case ID: {result.test_case_id}")
            
            # Compute baseline structural profiles
            basic_metrics = HeuristicMetrics.evaluate_basic(result.response)
            
            # Compute safety alignments (1.0 = Safe/Refused, 0.0 = Flagged/Vulnerable)
            safety_score = HeuristicMetrics.detect_refusal(result.response)
            
            # Compile everything into a unified reporting dictionary payload
            record = {
                "test_case_id": result.test_case_id,
                "category": result.category,
                "prompt": result.prompt,
                "expected_behavior": result.expected_behavior,
                "model_name": result.model_name,
                "response": result.response,
                "latency_seconds": result.latency_seconds,
                "error": result.error,
                "metrics": {
                    "is_empty": basic_metrics["is_empty"],
                    "character_count": basic_metrics["character_count"],
                    "word_count": basic_metrics["word_count"],
                    "safety_score": safety_score
                }
            }
            scored_records.append(record)
            
        logger.info(f"Engine execution completed successfully. Processed {len(scored_records)} records.")
        return scored_records