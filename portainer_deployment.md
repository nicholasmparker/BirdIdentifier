# Portainer Deployment Guide

After the GitHub Action builds and pushes the Docker image, follow these steps to deploy in Portainer:

1. **Create Stack File**:
   Create a new stack in Portainer and use this example configuration:

   ```yaml
   version: '3.8'

   services:
     birdidentifier:
       image: ghcr.io/nicholasmparker/birdidentifier:latest
       environment:
         - PYTHON_ENV=production
       ports:
         - "8000:8000"
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
         interval: 30s
         timeout: 5s
         retries: 3
         start_period: 10s
   ```

2. **Configure Registry**:
   - Use "ghcr.io" as the registry
   - No additional credentials needed if using GitHub-connected registry

3. **Environment Variables**:
    ```plaintext
    PYTHON_ENV=production
    ```

Note: Consider using a private registry if your model contains sensitive data
