from typing import Optional, Dict, Any
import os
import json
import asyncio

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Optional: for Vertex AI client
try:
    from google.cloud import aiplatform
    from google.cloud.aiplatform.gapic import prediction_service_client
except Exception:
    aiplatform = None
    prediction_service_client = None

app = FastAPI(title="COPILOT PRO V - AI Master Tool (Perplexity + Vertex AI)")

# Required environment variables (see README)
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
# Option A: Vertex REST endpoint (if using Generative API endpoint URL)
VERTEX_REST_URL = os.getenv("VERTEX_REST_URL", "")  # e.g. https://us-central1-aiplatform.googleapis.com/v1/projects/PROJECT/locations/LOCATION/publishers/google/models/MODEL:predict
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")  # optional API key for REST
# Option B: google-cloud-aiplatform (service account) via GOOGLE_APPLICATION_CREDENTIALS
GCP_PROJECT = os.getenv("GCP_PROJECT", "")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
VERTEX_ENDPOINT_ID = os.getenv("VERTEX_ENDPOINT_ID", "")  # if using a deployed endpoint

if not PERPLEXITY_API_KEY:
    print("Warning: PERPLEXITY_API_KEY not set. Perplexity calls will fail until set.")

class Query(BaseModel):
    prompt: str
    use_perplexity: Optional[bool] = True
    use_vertex: Optional[bool] = True
    vertex_instructions: Optional[str] = None

async def call_perplexity(prompt: str) -> Dict[str, Any]:
    """
    Minimal Perplexity API call — adapt to exact API shape/endpoint.
    IMPORTANT: Verify this endpoint with official Perplexity AI documentation
    as the API may have changed. Visit https://docs.perplexity.ai/ for current endpoints.
    """
    if not PERPLEXITY_API_KEY:
        raise RuntimeError("PERPLEXITY_API_KEY missing")

    # NOTE: Replace with the current Perplexity API endpoint and payload as needed.
    # This endpoint may need to be updated based on the latest Perplexity API documentation.
    url = "https://api.perplexity.ai/v1/answers"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"question": prompt, "num_results": 1}

    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        # Example expected shape: {"answer": "...", "sources": [...]}
        return data

def call_vertex_ai_sync(prompt: str, instructions: Optional[str] = None) -> Dict[str, Any]:
    """
    Two-mode Vertex call:
     - If google-cloud-aiplatform available and VERTEX_ENDPOINT_ID set -> use PredictionServiceClient
     - Else if VERTEX_REST_URL and GOOGLE_API_KEY provided -> do HTTP POST
     - Else raise error (user must configure credentials)
    """
    full_prompt = prompt if not instructions else f"{instructions}\n\n{prompt}"

    # Mode A: google-cloud-aiplatform PredictionServiceClient
    if prediction_service_client is not None and VERTEX_ENDPOINT_ID:
        client = prediction_service_client.PredictionServiceClient()
        endpoint = client.endpoint_path(GCP_PROJECT, GCP_LOCATION, VERTEX_ENDPOINT_ID)
        instance = {"content": full_prompt}
        instances = [instance]
        parameters = {}
        response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
        return {"predictions": [p for p in response.predictions]}

    # Mode B: REST call using GOOGLE_API_KEY and VERTEX_REST_URL
    if VERTEX_REST_URL and GOOGLE_API_KEY:
        headers = {"Content-Type": "application/json"}
        payload = {"instances": [{"content": full_prompt}], "parameters": {}}
        params = {"key": GOOGLE_API_KEY}
        r = httpx.post(VERTEX_REST_URL, headers=headers, json=payload, params=params, timeout=30.0)
        r.raise_for_status()
        return r.json()

    raise RuntimeError("Vertex AI not configured: set GOOGLE_APPLICATION_CREDENTIALS+VERTEX_ENDPOINT_ID or VERTEX_REST_URL+GOOGLE_API_KEY")

@app.post("/ask")
async def ask(q: Query):
    """
    Orchestrator endpoint:
    1) Optionally call Perplexity for a web-grounded sourced answer.
    2) Optionally call Vertex AI to transform/summarize/rewrite that result or answer directly.
    3) Return a merged result: {answer, sources, vertex_output}
    """
    try:
        perplexity_res = None
        vertex_res = None

        if q.use_perplexity:
            perplexity_res = await call_perplexity(q.prompt)

        if q.use_vertex:
            loop = asyncio.get_running_loop()
            # run CPU/network blocking call in threadpool
            vertex_res = await loop.run_in_executor(None, call_vertex_ai_sync, q.prompt, q.vertex_instructions)

        merged = {
            "prompt": q.prompt,
            "perplexity": perplexity_res,
            "vertex": vertex_res,
        }
        return merged

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ide")
async def ide_context(payload: Dict[str, Any]):
    """
    IDE endpoint used by the VS Code extension.
    Accepts JSON:
      { "context": "...", "question": "How do I refactor this?" }
    Returns the same orchestration applied to the question with context prepended.
    """
    context = payload.get("context", "")
    question = payload.get("question", "")
    if not question:
        raise HTTPException(status_code=400, detail="question required")
    composed = f"Project context:\n{context}\n\nQuestion:\n{question}"
    q = Query(prompt=composed, use_perplexity=True, use_vertex=True)
    return await ask(q)