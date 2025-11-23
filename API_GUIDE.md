# API Usage Guide - COPILOT PRO V

## Overview

COPILOT PRO V provides a RESTful API that orchestrates multiple AI services to deliver comprehensive answers for healthcare, consumer, and education industries.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API requires API keys to be configured in the `.env` file. No per-request authentication is needed for local development.

For production deployment, consider adding API key authentication middleware.

## Endpoints

### 1. Query Endpoint - `/ask`

This is the main endpoint for submitting queries to the AI orchestrator.

**Method:** `POST`

**URL:** `/ask`

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "prompt": "string",                    // Required: Your question or query
  "use_perplexity": true,                // Optional: Use Perplexity AI (default: true)
  "use_vertex": true,                    // Optional: Use Vertex AI (default: true)
  "vertex_instructions": "string"        // Optional: Custom instructions for Vertex AI
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What are the latest advancements in telemedicine?",
    "use_perplexity": true,
    "use_vertex": true,
    "vertex_instructions": "Focus on practical applications in rural healthcare"
  }'
```

**Success Response (200 OK):**
```json
{
  "prompt": "What are the latest advancements in telemedicine?",
  "perplexity": {
    "answer": "Recent advancements in telemedicine include...",
    "sources": [
      {
        "url": "https://example.com/article",
        "title": "Telemedicine Innovations 2025"
      }
    ]
  },
  "vertex": {
    "predictions": [
      "Detailed analysis of telemedicine in rural areas..."
    ]
  }
}
```

**Error Responses:**

- `400 Bad Request`: Invalid request format
- `500 Internal Server Error`: API call failed (check logs)

### 2. IDE Integration Endpoint - `/ide`

This endpoint is designed for IDE extensions and development tools to query with code context.

**Method:** `POST`

**URL:** `/ide`

**Request Body:**
```json
{
  "context": "string",    // Project or code context
  "question": "string"    // Question about the code
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/ide" \
  -H "Content-Type: application/json" \
  -d '{
    "context": "FastAPI application with database models using SQLAlchemy",
    "question": "How can I optimize database queries for large datasets?"
  }'
```

**Response:** Same format as `/ask` endpoint

## Industry-Specific Query Examples

### Healthcare Industry

```bash
# Medical Research
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Summarize recent clinical trials for Type 2 diabetes treatments",
    "use_perplexity": true,
    "use_vertex": true
  }'

# Patient Education
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain post-operative care after knee replacement surgery in simple terms",
    "vertex_instructions": "Use language appropriate for patients with 8th grade reading level"
  }'
```

### Consumer Services

```bash
# Product Recommendations
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What are the best sustainable alternatives to plastic packaging?",
    "use_perplexity": true
  }'

# Market Analysis
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analyze current trends in eco-friendly consumer products",
    "use_vertex": true,
    "vertex_instructions": "Focus on market data from the last 6 months"
  }'
```

### Education Industry

```bash
# Learning Content
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a lesson plan for teaching photosynthesis to 5th graders",
    "use_vertex": true,
    "vertex_instructions": "Include interactive activities and visual aids"
  }'

# Student Support
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain the Pythagorean theorem with real-world examples",
    "use_perplexity": true,
    "use_vertex": true
  }'
```

## Response Handling

### Successful Queries

Both services are optional. The response will contain:
- `prompt`: Echo of your original prompt
- `perplexity`: Results from Perplexity AI (if enabled and successful)
- `vertex`: Results from Vertex AI (if enabled and successful)

### Partial Success

If one service fails but another succeeds, you'll still get a 200 response with the successful service's data and `null` for the failed service.

### Complete Failure

If both services fail or there's a critical error, you'll receive a 500 error with details in the `detail` field.

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider:
- Adding rate limiting middleware
- Implementing request queuing
- Setting up caching for common queries

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 400 | Bad Request | Check request format and required fields |
| 401 | Unauthorized | Verify API keys in .env file |
| 500 | Internal Server Error | Check logs, verify API connectivity |
| 503 | Service Unavailable | One or more AI services are down |

## Best Practices

1. **Prompt Engineering**: Be specific and clear in your prompts
2. **Context**: Provide relevant context for better results
3. **Service Selection**: Choose appropriate services based on your needs:
   - Perplexity: Current information, web sources
   - Vertex AI: Advanced language processing, summarization
4. **Error Handling**: Always handle both partial and complete failures
5. **Caching**: Implement caching for repeated queries

## Integration Examples

### Python

```python
import requests

def query_ai(prompt: str, use_both: bool = True):
    url = "http://localhost:8000/ask"
    payload = {
        "prompt": prompt,
        "use_perplexity": use_both,
        "use_vertex": use_both
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

# Usage
result = query_ai("What are the symptoms of the common cold?")
print(result)
```

### JavaScript/Node.js

```javascript
async function queryAI(prompt, useBoth = true) {
    const response = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prompt: prompt,
            use_perplexity: useBoth,
            use_vertex: useBoth
        })
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Usage
queryAI('How does machine learning improve healthcare?')
    .then(result => console.log(result))
    .catch(error => console.error('Error:', error));
```

### cURL Scripts

```bash
#!/bin/bash
# Save as query.sh

PROMPT="${1:-What is artificial intelligence?}"

curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{
    \"prompt\": \"$PROMPT\",
    \"use_perplexity\": true,
    \"use_vertex\": true
  }" | jq '.'
```

## Monitoring and Logging

The application logs all requests and responses. Monitor logs for:
- API errors
- Performance issues
- Rate limiting needs

```bash
# View live logs
tail -f uvicorn.log

# Search for errors
grep -i error uvicorn.log
```

## Support

For API issues or questions:
1. Check the main documentation at `/docs`
2. Review error logs
3. Open an issue on GitHub
4. Contact the maintainer for licensing and commercial use

---

Copyright (c) 2025 Yadullah - All rights reserved
