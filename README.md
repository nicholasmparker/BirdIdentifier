# Bird Identifier API

A FastAPI service that identifies bird species in images using TensorFlow Lite.

This project is inspired by and builds upon [Who's At My Feeder](https://github.com/mmcc-xx/WhosAtMyFeeder) by mmcc-xx.

## Features

- Bird species identification from images
- Returns both common and scientific names
- Configurable confidence threshold
- Multiple prediction results support
- Container health monitoring
- CI/CD with GitHub Actions

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

## Deployment

The project uses GitHub Actions for CI/CD:
1. Automated tests and code quality checks
2. Docker image builds with multi-stage optimization
3. Security scanning with Trivy
4. Push to GitHub Container Registry

For production deployment instructions, see [portainer_deployment.md](portainer_deployment.md).

## Health Checks

The API provides a health check endpoint at `/api/v1/health` that returns:
- 200: Service is healthy
- 503: Service is unhealthy (ML model not loaded)

## License

MIT
