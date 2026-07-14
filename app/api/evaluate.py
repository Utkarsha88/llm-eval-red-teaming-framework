from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.evaluator.engine import EvaluationEngine
from app.utils.report_manager import ReportManager
from app.utils.logger import logger

router = APIRouter()
engine = EvaluationEngine()

class EvaluationRequest(BaseModel):
    models: List[str]
    datasets: List[str]
    concurrency_limit: Optional[int] = 3

@router.post("/evaluate", summary="Run a multi-model evaluation sweep")
async def trigger_evaluation(request: EvaluationRequest):
    logger.info(f"API received evaluation request for models: {request.models}")
    
    if not request.models or not request.datasets:
        raise HTTPException(status_code=400, detail="Must provide at least one model and one dataset.")

    master_results = {}

    for model_name in request.models:
        all_records = []
        for dataset_path in request.datasets:
            try:
                records = await engine.execute_run(
                    model_name=model_name,
                    dataset_path=dataset_path,
                    concurrency_limit=request.concurrency_limit
                )
                all_records.extend(records)
            except Exception as e:
                logger.error(f"API execution failed for {model_name} on {dataset_path}: {e}")
                
        if all_records:
            try:
                # Save the file to disk
                report_path = ReportManager.save_run(model_name, all_records)
                
                # Calculate the live scores for the UI Dashboard
                live_scores = ReportManager.calculate_aggregations(all_records)
                
                master_results[model_name] = {
                    "status": "success",
                    "report_file": report_path,
                    "records_processed": len(all_records),
                    "metrics": live_scores # <-- We added this for the UI!
                }
            except Exception as e:
                master_results[model_name] = {"status": "error", "message": str(e)}

    return {
        "message": "Evaluation sweep completed.",
        "results": master_results
    }