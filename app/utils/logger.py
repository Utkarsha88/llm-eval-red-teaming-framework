import sys
import logging
from app.utils.config import settings

def setup_logger(name: str = "llm-eval-RTF") -> logging.Logger:
    logger = logging.getLogger(name)
    
    # Prevent duplicate handlers if initialized multiple times
    if logger.handlers:
        return logger
        
    # Set the logging threshold based on environmental variables
    log_level_str = settings.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)
    
    # Define a clean, professional layout structure
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console Stream Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Export a primary root utility logger
logger = setup_logger()