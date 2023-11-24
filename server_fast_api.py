from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from agent_generator import *
import time
import asyncio
import os
import uvicorn

app = FastAPI()

# stream endpoint that receives json (question, session_id) and returns a streamed response
@app.post("/stream")
async def stream_response(data: dict):
    question = data["question"]
    session_id = data["session_id"]

    return StreamingResponse(run_agent(question, session_id), media_type='text/plain')


uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))