# COPILOT PRO V - AI MASTER TOOL

An advanced AI orchestration platform integrating multiple AI services (Perplexity AI, Google Vertex AI, and more) designed for health, consumer, and education industries.

## 🌟 Features

- **Multi-AI Integration**: Combines Perplexity AI for web-grounded research and Google Vertex AI for advanced language processing
- **Web Dashboard**: Beautiful, responsive UI for easy service management and monitoring
- **Industry-Focused**: Tailored solutions for healthcare, consumer services, and education sectors
- **RESTful API**: FastAPI-based backend for easy integration
- **Flexible Configuration**: Support for multiple authentication methods (service accounts, API keys)
- **Async Processing**: High-performance asynchronous request handling
- **IDE Integration**: Built-in endpoint for IDE extensions and development tools
- **Automated Startup**: Convenient shell script for quick deployment

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Valid API keys for Perplexity AI
- Google Cloud account with Vertex AI enabled (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AliMOla125/laughing-spoon.git
cd laughing-spoon
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. Run the application:

**Option A: Using the automated startup script (Recommended)**
```bash
# For Version 2 (Enhanced)
./start.sh v2

# Or for Version 1 (Basic)
./start.sh v1
```

**Option B: Manual startup**
```bash
# Using the basic version
uvicorn backend_main:app --reload

# Or using the enhanced version
uvicorn backend_main_Version2:app --reload
```

The API will be available at `http://localhost:8000`

### Web UI Dashboard

A web-based dashboard is available for easy interaction with the AI services:

1. Start the API server (as shown above)
2. Serve the web UI:
   ```bash
   # In a new terminal
   python -m http.server 8080
   ```
3. Open your browser to `http://localhost:8080/index.html`

The dashboard provides:
- Quick access to AI services (Perplexity AI, Google Vertex AI)
- Industry-specific solutions display (Healthcare, Education, Consumer)
- IDE integration status
- Visual status indicators for all services

## 📚 API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

#### POST /ask
General query endpoint that orchestrates calls to Perplexity AI and/or Vertex AI.

**Request Body:**
```json
{
  "prompt": "Your question here",
  "use_perplexity": true,
  "use_vertex": true,
  "vertex_instructions": "Optional custom instructions"
}
```

**Response:**
```json
{
  "prompt": "Your question",
  "perplexity": {
    "answer": "...",
    "sources": [...]
  },
  "vertex": {
    "predictions": [...]
  }
}
```

#### POST /ide
IDE integration endpoint for development tools.

**Request Body:**
```json
{
  "context": "Project or code context",
  "question": "Your question about the code"
}
```

## 🔧 Configuration

### Environment Variables

#### Required for Perplexity AI:
- `PERPLEXITY_API_KEY`: Your Perplexity API key

#### For Google Vertex AI (Option A - Service Account):
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account JSON
- `GCP_PROJECT`: Your GCP project ID
- `GCP_LOCATION`: GCP region (default: us-central1)
- `VERTEX_ENDPOINT_ID`: Vertex AI endpoint ID

#### For Google Vertex AI (Option B - API Key):
- `VERTEX_REST_URL`: Full REST endpoint URL
- `GOOGLE_API_KEY`: Your Google API key

## 📦 Project Structure

```
laughing-spoon/
├── backend_main.py           # Basic FastAPI orchestrator
├── backend_main_Version2.py  # Enhanced version with REST fallback
├── index.html               # Web UI dashboard
├── styles_Version2.css       # Minimal CSS styles
├── styles_Version2.1.css     # Full CSS styles for UI components
├── start.sh                 # Automated startup script
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment configuration
├── .gitignore               # Git ignore rules
├── README.md                # Main documentation
├── README_Version2.md        # Version 2 specific notes
├── API_GUIDE.md             # Detailed API usage guide
├── DEPLOYMENT.md            # Deployment instructions
├── QUICK_REFERENCE.md       # Quick command reference
└── LICENSE                  # License information
```

## 🏥 Industry Applications

### Healthcare
- Medical research assistance
- Patient education content generation
- Clinical documentation support
- Medical literature summarization

### Consumer Services
- Customer support automation
- Product recommendation systems
- Content personalization
- Market research analysis

### Education
- Personalized learning assistance
- Curriculum development support
- Student query resolution
- Educational content creation

## 🔐 Security & Licensing

Copyright (c) 2025 Yadullah

All rights reserved.

This software and associated documentation files (the "Software") are the exclusive property of Yadullah.

Permission is hereby granted to view and use the Software for personal, non-commercial purposes only.

### Restrictions:
- Redistribution, modification, sublicensing, or commercial use of the Software is strictly prohibited without prior written consent from Yadullah.
- Copying or launching derivative projects based on this Software is forbidden.
- Any unauthorized use will be subject to legal action under applicable copyright laws.

For licensing inquiries, please contact Yadullah.

## 🤝 Support

For questions, issues, or licensing inquiries, please open an issue in the GitHub repository or contact the maintainer.

## 🛠️ Development

### Running in Development Mode

```bash
# With auto-reload
uvicorn backend_main_Version2:app --reload --host 0.0.0.0 --port 8000

# View logs
tail -f uvicorn.log
```

### Testing

The API can be tested using the built-in Swagger UI at `/docs` or with curl:

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What are the latest developments in AI for healthcare?",
    "use_perplexity": true,
    "use_vertex": true
  }'
```

## 📝 Version History

- **Version 2**: Enhanced orchestrator with dual authentication support (service account + API key)
- **Version 1**: Basic Perplexity + Vertex AI integration

## 🌐 Additional Resources

- [Perplexity AI Documentation](https://docs.perplexity.ai/)
- [Google Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/) 
