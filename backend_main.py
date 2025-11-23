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
except Exception:
    aiplatform = None  # Keep graceful if library not installed

app = FastAPI(title="Perplexity + Vertex POC Orchestrator")

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
# Vertex AI settings: set GOOGLE_APPLICATION_CREDENTIALS file and these envs
GCP_PROJECT = os.getenv("GCP_PROJECT", "")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
VERTEX_ENDPOINT_ID = os.getenv("VERTEX_ENDPOINT_ID", "")  # or model id depending on client usage

if not PERPLEXITY_API_KEY:
    print("Warning: PERPLEXITY_API_KEY not set. Perplexity calls will fail until set.")

class Query(BaseModel):
    prompt: str
    use_perplexity: Optional[bool] = True
    use_vertex: Optional[bool] = True
    vertex_instructions: Optional[str] = None

async def call_perplexity(prompt: str) -> Dict[str, Any]:
    """
    Placeholder Perplexity API call.
    IMPORTANT: Verify this endpoint with official Perplexity AI documentation
    as the API may have changed. Visit https://docs.perplexity.ai/ for current endpoints.
    Adjust endpoint and payload to match current Perplexity API spec.
    """
    if not PERPLEXITY_API_KEY:
        raise RuntimeError("PERPLEXITY_API_KEY missing")

    # NOTE: This endpoint may need to be updated based on the latest Perplexity API documentation.
    url = "https://api.perplexity.ai/v1/answers"  # <-- verify with Perplexity docs
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"question": prompt, "num_results": 1}

    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
        # Adapt parsing based on returned schema
        # Example return structure: {"answer": "...", "sources": [...]}
        return data

def call_vertex_ai_sync(prompt: str, instructions: Optional[str] = None) -> Dict[str, Any]:
    """
    Example using google.cloud.aiplatform for a Vertex AI endpoint or model.
    You can replace with the new AI Studio / Generative API client when available.

    Requires:
    - pip install google-cloud-aiplatform
    - GOOGLE_APPLICATION_CREDENTIALS set to a service account JSON
    """
    if aiplatform is None:
        raise RuntimeError("google-cloud-aiplatform not installed")

    # Initialize client (this uses ADC)
    client = aiplatform.gapic.PredictionServiceClient()

    # Build endpoint resource name:
    endpoint = client.endpoint_path(GCP_PROJECT, GCP_LOCATION, VERTEX_ENDPOINT_ID)
    # Construct a simple predict request (adapt to model)
    instance = {"content": prompt if not instructions else f"{instructions}\n\n{prompt}"}
    instances = [instance]
    parameters = {}

    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
    # response.predictions contains model outputs; adapt parsing to model type
    return {"predictions": [p for p in response.predictions]}

@app.post("/ask")
async def ask(q: Query):
    """
    Orchestrator endpoint:
    1) Optionally call Perplexity for a sourced answer.
    2) Optionally call Vertex AI to transform/summarize.
    3) Return merged result.
    """
    try:
        perplexity_res = None
        vertex_res = None

        if q.use_perplexity:
            # Call Perplexity
            perplexity_res = await call_perplexity(q.prompt)

        if q.use_vertex:
            # If Vertex client is installed, make a sync call in thread pool
            loop = asyncio.get_running_loop()
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