# Deployment Guide - COPILOT PRO V

## Prerequisites

Before deploying COPILOT PRO V, ensure you have:

1. **Python Environment**
   - Python 3.8 or higher
   - pip package manager
   - Virtual environment support

2. **API Keys**
   - Perplexity AI API key (required for web-grounded queries)
   - Google Cloud credentials (optional, for Vertex AI)

3. **System Requirements**
   - Minimum 2GB RAM
   - Internet connectivity for API calls
   - Linux, macOS, or Windows with WSL

## Local Development Deployment

### Quick Start

1. **Clone and Navigate**
   ```bash
   git clone https://github.com/AliMOla125/laughing-spoon.git
   cd laughing-spoon
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   nano .env  # or use your preferred editor
   ```

3. **Run the Application**
   ```bash
   # Make the startup script executable (if not already)
   chmod +x start.sh
   
   # Start Version 2 (recommended)
   ./start.sh v2
   
   # Or start Version 1
   ./start.sh v1
   ```

4. **Access the Application**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Frontend: Open `index.html` in your browser

### Manual Setup

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the application
uvicorn backend_main_Version2:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

### Using Docker (Recommended for Production)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY backend_main_Version2.py .
COPY .env .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "backend_main_Version2:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
# Build Docker image
docker build -t copilot-pro-v .

# Run container
docker run -d -p 8000:8000 --env-file .env copilot-pro-v
```

### Using Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  copilot-pro-v:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

Deploy:

```bash
docker-compose up -d
```

### Cloud Deployment Options

#### Google Cloud Platform (Recommended for Vertex AI)

1. **Google Cloud Run**
   ```bash
   # Build and push to Google Container Registry
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/copilot-pro-v
   
   # Deploy to Cloud Run
   gcloud run deploy copilot-pro-v \
     --image gcr.io/YOUR_PROJECT_ID/copilot-pro-v \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars PERPLEXITY_API_KEY=your_key
   ```

2. **Google Kubernetes Engine (GKE)**
   - Create deployment and service YAML files
   - Use Kubernetes secrets for API keys
   - Configure ingress for external access

#### AWS Deployment

1. **AWS Elastic Beanstalk**
   ```bash
   # Create application
   eb init -p python-3.11 copilot-pro-v
   
   # Deploy
   eb create copilot-pro-v-env
   eb deploy
   ```

2. **AWS ECS/Fargate**
   - Push Docker image to ECR
   - Create ECS task definition
   - Deploy service with ALB

#### Azure Deployment

1. **Azure App Service**
   ```bash
   # Create resource group
   az group create --name copilot-pro-v-rg --location eastus
   
   # Create App Service plan
   az appservice plan create --name copilot-pro-v-plan \
     --resource-group copilot-pro-v-rg --sku B1 --is-linux
   
   # Create web app
   az webapp create --resource-group copilot-pro-v-rg \
     --plan copilot-pro-v-plan --name copilot-pro-v \
     --runtime "PYTHON:3.11"
   
   # Deploy
   az webapp up --name copilot-pro-v
   ```

### Reverse Proxy Setup (Nginx)

For production, use Nginx as a reverse proxy:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable SSL with Let's Encrypt:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Environment Configuration

### Required Environment Variables

```bash
# Perplexity AI (Required)
PERPLEXITY_API_KEY=your_perplexity_api_key

# Google Cloud / Vertex AI (Optional)
# Option A: Service Account
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GCP_PROJECT=your-gcp-project-id
GCP_LOCATION=us-central1
VERTEX_ENDPOINT_ID=your-endpoint-id

# Option B: API Key
VERTEX_REST_URL=https://...
GOOGLE_API_KEY=your_google_api_key

# Server Configuration (Optional)
HOST=0.0.0.0
PORT=8000
```

## Monitoring and Logging

### Application Logs

```bash
# View live logs
tail -f uvicorn.log

# Search for errors
grep -i error uvicorn.log

# Monitor API calls
grep "POST /ask" uvicorn.log
```

### Health Check Endpoint

Add to your application:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "perplexity": bool(PERPLEXITY_API_KEY),
        "vertex": bool(VERTEX_ENDPOINT_ID or VERTEX_REST_URL)
    }
```

### Performance Monitoring

Consider integrating:
- Prometheus for metrics
- Grafana for visualization
- Sentry for error tracking
- Google Cloud Monitoring (if on GCP)

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**: Use Nginx, HAProxy, or cloud load balancers
2. **Multiple Instances**: Deploy multiple app instances
3. **Session Management**: Keep API stateless
4. **Caching**: Implement Redis for common queries

### Vertical Scaling

- Increase CPU/RAM for the container
- Use production ASGI server (Gunicorn with uvicorn workers)

Example with Gunicorn:

```bash
gunicorn backend_main_Version2:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Security Best Practices

1. **API Keys**: Never commit .env files; use secrets management
2. **HTTPS**: Always use SSL/TLS in production
3. **Rate Limiting**: Implement rate limiting middleware
4. **CORS**: Configure appropriate CORS policies
5. **Authentication**: Add API key authentication for production
6. **Network Security**: Use VPC, security groups, firewall rules
7. **Regular Updates**: Keep dependencies updated

## Backup and Disaster Recovery

1. **Configuration Backup**: Version control .env.example
2. **Database Backup**: If adding persistence, backup regularly
3. **Multi-Region**: Deploy in multiple regions for high availability
4. **Monitoring Alerts**: Set up alerts for downtime

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill process
   kill -9 PID
   ```

2. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install --force-reinstall -r requirements.txt
   ```

3. **API Key Errors**
   - Verify .env file exists and contains valid keys
   - Check environment variables are loaded
   - Ensure no trailing spaces in API keys

4. **Vertex AI Connection Issues**
   - Verify GOOGLE_APPLICATION_CREDENTIALS path
   - Check GCP project permissions
   - Ensure Vertex AI API is enabled

## Performance Optimization

1. **Connection Pooling**: Configure httpx client with connection pool
2. **Async Operations**: Leverage async/await properly
3. **Caching**: Cache common queries with Redis
4. **CDN**: Use CDN for static frontend files
5. **Compression**: Enable gzip compression

## Compliance and Legal

- Ensure compliance with data protection laws (GDPR, HIPAA for healthcare)
- Review and comply with AI service provider terms
- Implement proper data handling and privacy policies
- Maintain audit logs for regulatory compliance

---

Copyright (c) 2025 Yadullah - All rights reserved

For licensing inquiries or commercial deployment, contact the maintainer.
