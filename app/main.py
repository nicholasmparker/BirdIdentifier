"""FastAPI application entry point.

This module initializes the FastAPI application, configures middleware,
and sets up API routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config import Settings

# Load settings
settings = Settings()

# Create FastAPI app
app = FastAPI(
    title="BirdIdentifier API",
    description="A REST API service for identifying birds in images",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring service status.

    Returns:
        dict: Status response with "healthy" status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
