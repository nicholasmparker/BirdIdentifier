"""Configuration settings for the Bird Identifier API.

This module handles environment variables and application settings using Pydantic.
"""

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and configuration.

    Attributes:
        ENVIRONMENT: Runtime environment (development/staging/production)
        DEBUG: Debug mode flag
        API_V1_STR: API version prefix
        MODEL_PATH: Path to TFLite model file
        MAX_IMAGE_SIZE: Maximum allowed image size in bytes
        ALLOWED_EXTENSIONS: Set of allowed image file extensions
    """

    # API Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"

    # ML Model Settings
    MODEL_PATH: str = "models/model.tflite"

    # Image Settings
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set[str] = {"jpg", "jpeg", "png"}

    @validator("ENVIRONMENT")
    def validate_environment(cls, v: str) -> str:
        """Validate the environment setting.

        Args:
            v: Environment value to validate

        Returns:
            Validated environment string

        Raises:
            ValueError: If environment is not one of: development, staging, production
        """
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
