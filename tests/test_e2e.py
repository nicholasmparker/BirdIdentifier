"""End-to-end tests for the Bird Identifier API.

This module contains integration tests that verify the complete
functionality of the API using real image data.
"""

import os

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_e2e_bird_identification():
    """End-to-end test for bird identification using a real image."""
    # Path to test image
    image_path = os.path.join("tests", "assets", "test_bird.jpg")
    abs_path = os.path.abspath(image_path)
    print(f"\nLooking for test image at: {abs_path}")
    print(f"Current working directory: {os.getcwd()}")
    print("Directory contents:")
    print(os.listdir("tests/assets"))

    # Ensure the test image exists
    msg = "Test image not found at " + image_path
    assert os.path.exists(image_path), msg

    # Read the image file
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Prepare the request
    files = {"image": ("test_bird.jpg", image_data, "image/jpeg")}
    params = {"threshold": 0.5, "max_results": 3}

    # Make the request
    response = client.post("/api/v1/identify", files=files, params=params)

    # Check response
    if response.status_code != 200:
        print(f"\nResponse status: {response.status_code}")
        print(f"Response body: {response.text}")
    assert response.status_code == 200

    # Parse response
    data = response.json()

    # Verify response structure
    assert "predictions" in data
    assert "processing_time" in data
    assert "timestamp" in data

    # Verify predictions
    predictions = data["predictions"]
    assert isinstance(predictions, list)
    assert len(predictions) > 0

    # Verify first prediction structure
    first_prediction = predictions[0]
    assert "species" in first_prediction
    assert "confidence" in first_prediction
    assert "scientific_name" in first_prediction

    # Verify confidence threshold
    assert all(pred["confidence"] >= 0.5 for pred in predictions)

    # Verify max results
    assert len(predictions) <= 3

    # Print results for manual verification
    print("\nTest Results:")
    print(f"Number of predictions: {len(predictions)}")
    for pred in predictions:
        print(f"Species: {pred['species']}")
        print(f"Confidence: {pred['confidence']:.2f}")
        print(f"Scientific name: {pred['scientific_name']}")
        print("---")
