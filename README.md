# Bird Identifier API

A FastAPI service that identifies bird species in images using TensorFlow Lite.

## Features

- Bird species identification from images
- Returns both common and scientific names
- Configurable confidence threshold
- Multiple prediction results support

## Setup

1. Clone the repository:
```bash
git clone https://github.com/nicholasmparker/BirdIdentifier.git
cd BirdIdentifier
```

2. Build and run with Docker:
```bash
docker compose up --build
```

3. Access the API documentation at:
```
http://localhost:8000/api/v1/docs
```

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Install pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
make test
```

## API Usage

Send a POST request to `/api/v1/identify` with:
- An image file
- Optional `threshold` parameter (default: 0.5)
- Optional `max_results` parameter (default: 3)

Example response:
```json
{
  "predictions": [
    {
      "species": "Northern Cardinal",
      "scientific_name": "Cardinalis cardinalis",
      "confidence": 0.88
    }
  ],
  "processing_time": 0.15,
  "timestamp": "2024-02-04T15:30:00Z"
}
```

## License

MIT
