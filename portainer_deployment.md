# Portainer Deployment Guide

After the GitHub Action builds and pushes the Docker image, follow these steps to deploy in Portainer:

1. **Create Stack File**:
   Create a new stack in Portainer and use this example configuration:

   ```yaml
   version: '3.8'

   services:
     birdidentifier:
       image: ghcr.io/your-org/birdidentifier:latest
       environment:
         - PYTHON_ENV=production
         - DATABASE_URL=postgres://user:pass@host:port/db
         - MODEL_PATH=/app/models/model.tflite
       ports:
         - "8000:8000"
       volumes:
         - ./models:/app/models
       deploy:
         replicas: 2
         resources:
           limits:
             cpus: '2'
             memory: 4G
           reservations:
             cpus: '1'
             memory: 2G
         restart_policy:
           condition: unless-stopped
         healthcheck:
           test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
           interval: 30s
           timeout: 5s
           retries: 3
           start_period: 10s

   networks:
     default:
       driver: overlay
   ```

2. **Configure Registry**:
   - Use "ghcr.io" as the registry
   - No additional credentials needed if using GitHub-connected registry

3. **Environment Variables**:
   ```plaintext
   PYTHON_ENV=production
   DATABASE_URL=postgres://user:pass@host:port/db
   MODEL_PATH=/app/models/model.tflite
   ```

4. **Resource Requirements**:
   - Minimum per replica: 1 vCPU, 2GB RAM
   - Recommended per replica: 2 vCPU, 4GB RAM
   - Storage: 1GB (+ space for model files)
   - Network: Overlay network for swarm mode

5. **Health Monitoring**:
   - Health check endpoint: `/api/v1/health`
   - Monitoring interval: 30s
   - Timeout: 5s
   - Retries: 3
   - Start period: 10s

For production deployments, ensure you've set these secrets in GitHub:
- Database credentials
- Any API keys used by the application

Note: Adjust the number of replicas, resource limits, and other parameters based on your specific needs and infrastructure capacity.
