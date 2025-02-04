"""Machine learning service for bird species identification.

This module handles TensorFlow Lite model loading, image preprocessing,
and bird species prediction using computer vision.
"""

import io
from typing import List

import numpy as np
from PIL import Image, ImageOps
from tflite_support.task import core, processor, vision

from app.config import settings
from app.queries import get_common_name
from app.schemas.bird import BirdPrediction


class MLService:
    """Service for bird species identification using TensorFlow Lite.

    This service handles:
    - Loading and managing the TFLite model
    - Image preprocessing and inference
    - Converting model outputs to bird predictions
    """

    def __init__(self):
        """Initialize the ML service.

        Sets up the TensorFlow Lite classifier and species data.
        Falls back to development mode if model loading fails.
        """
        self.classifier = None
        self.species_list = None
        self.scientific_names = None
        self._load_model()
        self._initialize_species_data()

        # In development mode, initialize with test species
        if settings.ENVIRONMENT == "development":
            self.species_list = [common for _, common in self.DEV_BIRDS]

    def _load_model(self):
        """Load and initialize the TFLite model for bird classification.

        Raises:
            Exception: If model loading fails in production mode
        """
        try:
            print(f"Attempting to load model from: {settings.MODEL_PATH}")
            # Initialize the image classification model
            base_options = core.BaseOptions(
                file_name=settings.MODEL_PATH, use_coral=False, num_threads=4
            )
            classification_options = processor.ClassificationOptions(
                # At least 1, but allow for more if requested
                max_results=max(3, 1),
                score_threshold=0.0,  # We'll filter by threshold later
            )
            options = vision.ImageClassifierOptions(
                base_options=base_options,
                classification_options=classification_options,
            )

            # Create classifier
            self.classifier = vision.ImageClassifier.create_from_options(
                options
            )
            print("Successfully loaded TFLite model")
        except Exception as e:
            # For development, we'll create a dummy model
            if settings.ENVIRONMENT == "development":
                print("Failed to load model, falling back to development mode")
                self.classifier = None
            else:
                print(f"Failed to load model with error: {str(e)}")
                raise Exception(f"Failed to load model: {str(e)}")

    def _initialize_species_data(self):
        """Initialize bird species data.

        Note: Not needed anymore since we use the model's display_name
        directly.
        """
        pass

    async def _preprocess_image(self, image_data: bytes) -> np.ndarray:
        """Preprocess an image for model input.

        Args:
            image_data: Raw image bytes

        Returns:
            numpy.ndarray: Preprocessed image array (224x224x3 uint8)
        """
        image = Image.open(io.BytesIO(image_data))
        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Resize while maintaining aspect ratio
        max_size = (224, 224)
        image.thumbnail(max_size)

        # Pad the image to fill the remaining space
        padded_image = ImageOps.expand(
            image,
            border=(
                (max_size[0] - image.size[0]) // 2,
                (max_size[1] - image.size[1]) // 2,
            ),
            fill="black",
        )

        return np.array(padded_image, dtype=np.uint8)

    async def predict(
        self, image_data: bytes, threshold: float, max_results: int
    ) -> List[BirdPrediction]:
        """Process an image and return bird species predictions.

        Args:
            image_data: Raw image bytes to process
            threshold: Minimum confidence threshold (0-1)
            max_results: Maximum number of predictions to return

        Returns:
            List of BirdPrediction objects, sorted by confidence

        Raises:
            Exception: If image processing or inference fails
        """
        # In development, return dummy predictions
        if self.classifier is None:
            print("Using development mode for predictions (random data)")
            import random

            predictions = []
            species = random.sample(
                self.DEV_BIRDS, min(max_results, len(self.DEV_BIRDS))
            )
            for scientific, common in species:
                confidence = random.uniform(threshold, 1.0)
                predictions.append(
                    BirdPrediction(
                        species=common,
                        confidence=confidence,
                        scientific_name=scientific,
                    )
                )
            return sorted(
                predictions, key=lambda x: x.confidence, reverse=True
            )

        # Production prediction logic
        try:
            # Preprocess image
            processed_image = await self._preprocess_image(image_data)

            print("Starting TFLite inference process...")
            # Create TensorImage from numpy array
            tensor_image = vision.TensorImage.create_from_array(
                processed_image
            )

            # Run classification
            print("Running classification...")
            categories = self.classifier.classify(tensor_image)
            print(
                f"Got {len(categories.classifications[0].categories)} categories"
            )

            # Process results
            results = []
            for category in categories.classifications[0].categories:
                print(
                    f"Category: index={category.index}, score={category.score}"
                )
                if (
                    category.score >= threshold and category.index != 964
                ):  # 964 is background
                    results.append(
                        BirdPrediction(
                            species=get_common_name(category.display_name),
                            confidence=float(category.score),
                            scientific_name=category.display_name,
                        )
                    )
            print(f"Found {len(results)} results above threshold {threshold}")

            # Sort by confidence and limit results
            results.sort(key=lambda x: x.confidence, reverse=True)
            return results[:max_results]

        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    # Common development birds
    DEV_BIRDS = [
        ("Cardinalis cardinalis", "Northern Cardinal"),
        ("Cyanocitta cristata", "Blue Jay"),
        ("Turdus migratorius", "American Robin"),
        ("Haemorhous mexicanus", "House Finch"),
        ("Poecile atricapillus", "Black-capped Chickadee"),
    ]

    async def get_supported_species(self) -> List[str]:
        """Get a list of all supported bird species.

        Returns:
            List of bird species names that can be identified by the model
        """
        if self.classifier is None:
            # In development mode, return our test species
            return [common for _, common in self.DEV_BIRDS]

        # In production, return species list or empty list if not initialized
        return self.species_list or []
