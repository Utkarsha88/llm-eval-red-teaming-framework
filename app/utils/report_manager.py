import json
import os
from datetime import datetime
from typing import List, Dict, Any
from app.utils.logger import logger

class ReportManager:
    """
    Handles saving evaluation metrics to disk and calculating aggregations.
    """

    @staticmethod
    def calculate_aggregations(records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compiles list-level telemetry into structured aggregate insights.
        """
        if not records:
            return {}

        total_cases = len(records)
        successful_runs = sum(1 for r in records if r["error"] is None)
        
        # Calculate metric averages
        latencies = [r["latency_seconds"] for r in records if r["latency_seconds"] is not None]
        avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else 0.0
        
        safety_scores = [r["metrics"]["safety_score"] for r in records]
        avg_safety = round((sum(safety_scores) / total_cases) * 100, 2) if total_cases else 0.0

        # Group data counts by category profiles
        category_summary: Dict[str, Dict[str, Any]] = {}
        for r in records:
            cat = r["category"]
            if cat not in category_summary:
                category_summary[cat] = {"count": 0, "total_safety": 0.0}
            category_summary[cat]["count"] += 1
            category_summary[cat]["total_safety"] += r["metrics"]["safety_score"]

        # Calculate localized percentages per category
        category_metrics = {}
        for cat, data in category_summary.items():
            category_metrics[cat] = {
                "test_count": data["count"],
                "safety_alignment_pct": round((data["total_safety"] / data["count"]) * 100, 2)
            }

        return {
            "summary": {
                "total_test_cases": total_cases,
                "successful_executions": successful_runs,
                "failed_executions": total_cases - successful_runs,
                "average_latency_seconds": avg_latency,
                "overall_safety_alignment_pct": avg_safety
            },
            "breakdown_by_category": category_metrics
        }

    @staticmethod
    def save_run(model_name: str, records: List[Dict[str, Any]]) -> str:
        """
        Persists raw execution metrics and aggregations into a unified JSON file.
        
        Returns:
            str: Path to the generated report artifact.
        """
        aggregations = ReportManager.calculate_aggregations(records)
        
        # Build clean timestamped file naming structures
        safe_model_name = model_name.replace("/", "_").replace(":", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{safe_model_name}_{timestamp}.json"
        
        output_directory = os.path.join("outputs", "json")
        os.makedirs(output_directory, exist_ok=True)
        
        full_path = os.path.join(output_directory, filename)
        
        payload = {
            "metadata": {
                "model_name": model_name,
                "generated_at": datetime.now().isoformat(),
            },
            "aggregations": aggregations,
            "detailed_records": records
        }
        
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            logger.info(f"Successfully exported evaluation report to: {full_path}")
            return full_path
        except Exception as e:
            logger.error(f"Failed to write evaluation report to disk: {str(e)}")
            raise e