"""API endpoint tests for the Bird Identifier service.

This module contains integration tests for the FastAPI endpoints,
testing bird identification, health checks, and species listing.
"""

import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    # Create a simple RGB image
    img = Image.new("RGB", (224, 224), color="red")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_identify_endpoint(sample_image):
    """Test the bird identification endpoint."""
    files = {"image": ("test.png", sample_image, "image/png")}
    params = {"threshold": 0.5, "max_results": 3}
    response = client.post("/api/v1/identify", files=files, params=params)
    assert response.status_code == 200

    data = response.json()
    assert "predictions" in data
    assert "processing_time" in data
    assert "timestamp" in data

    # Check predictions structure
    predictions = data["predictions"]
    assert isinstance(predictions, list)
    if predictions:
        prediction = predictions[0]
        assert "species" in prediction
        assert "confidence" in prediction
        assert "scientific_name" in prediction
        assert 0 <= prediction["confidence"] <= 1


def test_identify_invalid_file():
    """Test the endpoint with invalid file type."""
    files = {"image": ("test.txt", b"not an image", "text/plain")}
    params = {"threshold": 0.5, "max_results": 3}
    response = client.post("/api/v1/identify", files=files, params=params)
    assert response.status_code == 400


def test_species_list():
    """Test the species list endpoint in development mode."""
    response = client.get("/api/v1/species")
    assert response.status_code == 200

    species_list = response.json()
    assert isinstance(species_list, list)
    # In development mode, we expect our test species
    expected_species = [
        "Northern Cardinal",
        "Blue Jay",
        "American Robin",
        "House Finch",
        "Black-capped Chickadee",
    ]
    assert species_list == expected_species


def test_identify_with_parameters(sample_image):
    """Test identification with custom threshold and max_results."""
    files = {"image": ("test.png", sample_image, "image/png")}
    params = {"threshold": 0.8, "max_results": 2}
    response = client.post("/api/v1/identify", files=files, params=params)
    assert response.status_code == 200

    data = response.json()
    predictions = data["predictions"]
    assert len(predictions) <= 2
    if predictions:
        assert all(pred["confidence"] >= 0.8 for pred in predictions)
