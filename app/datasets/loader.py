import json
from pathlib import Path
from typing import List
from pydantic import BaseModel, ValidationError
from app.utils.logger import logger

# 1. Define the strict schema for our test cases
class EvaluationTestCase(BaseModel):
    """
    Pydantic model representing a single evaluation prompt.
    Ensures every test case loaded from JSON has the required fields.
    """
    id: str
    category: str
    prompt: str
    expected_behavior: str

# 2. Define the loader utility
class DatasetLoader:
    """Utility class to load and validate JSON evaluation datasets."""
    
    @staticmethod
    def load(file_path: str) -> List[EvaluationTestCase]:
        """
        Reads a JSON file and parses it into a list of EvaluationTestCase objects.
        """
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"Dataset file not found: {file_path}")
            raise FileNotFoundError(f"Cannot find dataset at {file_path}")
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                
            # Validate the raw list of dictionaries against our Pydantic model
            # This is a list comprehension that parses each item
            test_cases = [EvaluationTestCase(**item) for item in raw_data]
            
            logger.info(f"Successfully loaded {len(test_cases)} test cases from {path.name}")
            return test_cases
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in {file_path}: {str(e)}")
            raise ValueError(f"Failed to parse JSON in {file_path}")
            
        except ValidationError as e:
            logger.error(f"Schema validation failed in {file_path}. Missing or invalid fields.")
            # Print the specific Pydantic error so the user knows exactly what to fix
            print(e)
            raise ValueError(f"Dataset {file_path} does not match the required schema.")