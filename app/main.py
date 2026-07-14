
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logger import logger
from app.utils.config import settings

# Import the evaluation router we just built
from app.api.evaluate import router as eval_router

# Initialize the core FastAPI instance
app = FastAPI(
    title="SentinelLLM API",
    description="Automated evaluation and red teaming backend engine for Large Language Models.",
    version="1.0.0"
)

# Enable Cross-Origin Resource Sharing (CORS) so our UI frontend can communicate safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global custom exception handling boundary to keep the API from crashing silently
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled system exception routed on path {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal processing exception encountered within the Sentinel engine.",
            "details": str(exc)
        }
    )

# Baseline operational health check endpoint
@app.get("/api/health", tags=["System Diagnostics"])
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "engine": "SentinelLLM v1.0.0"
    }

# Connect the evaluation endpoints to the main application
app.include_router(eval_router, prefix="/api")