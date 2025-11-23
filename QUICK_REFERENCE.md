# Quick Reference - COPILOT PRO V

## 🚀 Quick Start Commands

```bash
# Setup
git clone https://github.com/AliMOla125/laughing-spoon.git
cd laughing-spoon
cp .env.example .env
# Edit .env with your API keys

# Run
./start.sh v2
```

## 📡 API Endpoints

### Main Query Endpoint
```bash
POST http://localhost:8000/ask

{
  "prompt": "Your question",
  "use_perplexity": true,
  "use_vertex": true,
  "vertex_instructions": "Optional instructions"
}
```

### IDE Integration
```bash
POST http://localhost:8000/ide

{
  "context": "Code or project context",
  "question": "Your question"
}
```

## 🔑 Environment Variables

```bash
# Required
PERPLEXITY_API_KEY=xxx

# Optional (Vertex AI)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GCP_PROJECT=your-project-id
GCP_LOCATION=us-central1
VERTEX_ENDPOINT_ID=your-endpoint-id

# Or use REST
VERTEX_REST_URL=https://...
GOOGLE_API_KEY=xxx
```

## 🧪 Testing Examples

### Healthcare Query
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the latest COVID-19 treatment guidelines?"}'
```

### Education Query
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing for high school students"}'
```

### Consumer Query
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Compare electric vs hybrid vehicles in 2025"}'
```

## 📚 Documentation Links

- **Main README**: `README.md`
- **API Guide**: `API_GUIDE.md`
- **Deployment**: `DEPLOYMENT.md`
- **License**: `LICENSE`
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠️ Common Commands

```bash
# Start application
./start.sh v2                           # Version 2 (recommended)
./start.sh v1                           # Version 1

# Manual start
source venv/bin/activate
uvicorn backend_main_Version2:app --reload

# Check syntax
python3 -m py_compile backend_main*.py

# View logs
tail -f uvicorn.log

# Install dependencies
pip install -r requirements.txt
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | `lsof -i :8000` then `kill -9 PID` |
| Import errors | `pip install --force-reinstall -r requirements.txt` |
| API key error | Check `.env` file exists and has valid keys |
| Vertex AI error | Verify GOOGLE_APPLICATION_CREDENTIALS path |

## 📦 Project Structure

```
laughing-spoon/
├── backend_main.py              # Basic version
├── backend_main_Version2.py     # Enhanced version ⭐
├── index.html                   # Frontend UI
├── styles_Version2.1.css        # Full styles ⭐
├── requirements.txt             # Dependencies
├── .env.example                 # Config template
├── start.sh                     # Startup script ⭐
├── README.md                    # Main docs
├── API_GUIDE.md                 # API reference
├── DEPLOYMENT.md                # Deploy guide
└── LICENSE                      # Copyright
```

## 🎯 Industry Use Cases

### Healthcare
- Medical research queries
- Patient education content
- Clinical documentation
- Drug interaction checks

### Education
- Lesson plan generation
- Student query assistance
- Educational content creation
- Homework help

### Consumer
- Product recommendations
- Market analysis
- Customer support
- Content personalization

## 🔐 Security Checklist

- [x] API keys in .env (not hardcoded)
- [x] .gitignore excludes credentials
- [x] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Add API authentication
- [ ] Enable CORS properly
- [ ] Regular security updates

## 📞 Support

- **Issues**: GitHub Issues
- **Licensing**: Contact Yadullah
- **Documentation**: See README.md
- **API Docs**: http://localhost:8000/docs

## 🏷️ Version Info

- **Current**: v2.0
- **Python**: 3.8+
- **Framework**: FastAPI
- **AI Services**: Perplexity AI, Google Vertex AI

---

**Copyright (c) 2025 Yadullah** - All rights reserved

For commercial use or licensing inquiries, contact the maintainer.
