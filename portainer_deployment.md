# Portainer Deployment Guide

After the GitHub Action builds and pushes the Docker image, follow these steps to deploy in Portainer:

1. **Pull Image from GHCR**:
   ```bash
   ghcr.io/your-org/birdidentifier:$GITHUB_SHA
   ```
   - Use "ghcr.io" as the registry (no additional credentials needed if using GitHub-connected registry)

2. **Required Environment Variables**:
   ```plaintext
   PYTHON_ENV=production
   DATABASE_URL=postgres://user:pass@host:port/db
   MODEL_PATH=/app/models/model.tflite
   ```

3. **Portainer Configuration**:
   - Health check endpoint: `/api/v1/health`
   - Expose port: 8000 (TCP)
   - Set restart policy: `unless-stopped`

4. **Recommended Resources**:
   - Minimum: 2 vCPU, 4GB RAM
   - Storage: 1GB (+ space for model files)

For production deployments, ensure you've set these secrets in GitHub:
- Database credentials
- Any API keys used by the application
