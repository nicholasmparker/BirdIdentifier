"""Pydantic models for bird identification API responses.

This module defines the data models for bird predictions and API responses.
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class BirdPrediction(BaseModel):
    """A single bird species prediction.

    Attributes:
        species: Common name of the bird species
        confidence: Prediction confidence score (0.0 to 1.0)
        scientific_name: Scientific (Latin) name of the bird species
    """

    species: str = Field(..., description="Common name of the bird species")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score of the prediction"
    )
    scientific_name: str = Field(
        ..., description="Scientific name of the bird species"
    )


class BirdResponse(BaseModel):
    """API response for bird identification.

    Attributes:
        predictions: List of bird predictions
        processing_time: Time taken to process the image
        timestamp: UTC timestamp of the prediction
    """

    predictions: List[BirdPrediction] = Field(
        ..., description="List of bird predictions"
    )
    processing_time: float = Field(
        ..., description="Time taken to process the image in seconds"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of the prediction",
    )

    class Config:
        """Pydantic configuration for datetime serialization."""

        json_encoders = {datetime: lambda v: v.isoformat()}
