"""API router for bird identification endpoints.

This module handles image upload, bird identification, and species listing.
"""

from typing import List

from fastapi import APIRouter, File, HTTPException, Response, UploadFile

from app.config import settings
from app.schemas.bird import BirdResponse
from app.services.ml import MLService

api_router = APIRouter()
ml_service = MLService()


@api_router.get("/health")
async def health_check():
    """Health check endpoint for container monitoring.

    Returns:
        Response with 200 status if service is healthy
    """
    try:
        # Verify ML service is initialized
        if (
            ml_service.classifier is None
            and settings.ENVIRONMENT != "development"
        ):
            return Response(
                content="ML service not initialized", status_code=503
            )
        return Response(status_code=200)
    except Exception:
        return Response(content="Service unhealthy", status_code=503)


@api_router.post("/identify", response_model=BirdResponse)
async def identify_bird(
    image: UploadFile = File(...),
    threshold: float = ...,  # Required parameter
    max_results: int = ...,  # Required parameter
):
    """Identify birds in the uploaded image.

    Args:
        image: Image file (jpg, jpeg, or png)
        threshold: Minimum confidence threshold (0-1)
        max_results: Maximum number of predictions to return

    Returns:
        BirdResponse containing predictions and metadata

    Raises:
        HTTPException: For invalid parameters or processing errors
    """
    # Validate parameters
    if not 0 <= threshold <= 1:
        raise HTTPException(
            status_code=400, detail="Threshold must be between 0 and 1"
        )

    if max_results < 1:
        raise HTTPException(
            status_code=400, detail="max_results must be greater than 0"
        )

    # Validate file extension
    file_extension = image.filename.split(".")[-1].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        allowed = ", ".join(settings.ALLOWED_EXTENSIONS)
        raise HTTPException(
            status_code=400, detail=f"File extension must be one of: {allowed}"
        )

    try:
        # Read image content
        content = await image.read()
        max_mb = settings.MAX_IMAGE_SIZE // (1024 * 1024)
        if len(content) > settings.MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum of {max_mb}MB",
            )

        # Get predictions from ML service
        predictions = await ml_service.predict(
            image_data=content, threshold=threshold, max_results=max_results
        )

        return BirdResponse(
            predictions=predictions,
            processing_time=0.0,  # TODO: Add actual processing time
        )

    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Error processing image: {str(e)}"
        print(error_msg)  # Print for test output
        raise HTTPException(status_code=500, detail=error_msg)


@api_router.get("/species", response_model=List[str])
async def list_species():
    """Get a list of all supported bird species.

    Returns:
        List of bird species names that can be identified

    Raises:
        HTTPException: If there's an error fetching the species list
    """
    try:
        return await ml_service.get_supported_species()
    except Exception as e:
        error_msg = f"Error fetching species list: {str(e)}"
        print(error_msg)  # Print for test output
        raise HTTPException(status_code=500, detail=error_msg)
