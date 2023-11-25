from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from agent_generator import *
import time
import asyncio
import os
import uvicorn

from development import *

app = FastAPI()

# stream endpoint that receives json (question, session_id) and returns a streamed response
@app.post("/stream")
async def stream_response(data: dict):
    question = data["question"]
    session_id = data["session_id"]

    return StreamingResponse(run_agent(question, session_id), media_type='text/plain')

@app.post("/drug-interactions")
async def drug_interactions(drugs: dict):

    try:
        drugs = drugs["drugs"]
        if not isinstance(drugs, list):
            raise HTTPException(status_code=400, detail="Invalid payload. 'drugs' should be a list.")

        interactions = describe_interactions(drugs)

        if not interactions["pairs"]:

            return {
                "drug_interactions": False,
                "explanation": "No interactions found"
            }

        explanation = explain_interactions(interactions)

        return {
            "drug_interactions": True,
            "explanation": explanation
        }
    except:
        raise HTTPException(status_code=400, detail="Invalid payload. 'drugs' should be a list.")

uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))