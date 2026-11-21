
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
import asyncio
import uuid
from fastapi import FastAPI

app = FastAPI(title="Context Aware Chatbot")

from chatbot import get_response

app = FastAPI(title="Context Aware Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Separate history for every conversation
conversations = {}

MAX_MESSAGES = 10

class ChatRequest(BaseModel):
    conversation_id: str | None = None
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    conversation_id = (
        request.conversation_id or str(uuid.uuid4())
    )

    history = conversations.get(conversation_id, [])

    # Include the new message without changing saved history yet
    updated_history = history + [{
        "role": "user",
        "content": request.message
    }]

    # Retain the last 10 messages for the model
    context = updated_history[-MAX_MESSAGES:]

    try:
        answer = await asyncio.wait_for(
            run_in_threadpool(get_response, context),
            timeout=35
        )

        # Save messages only after successful response
        updated_history.append({
            "role": "assistant",
            "content": answer
        })

        conversations[conversation_id] = updated_history[-MAX_MESSAGES:]

        return {
            "conversation_id": conversation_id,
            "response": answer
        }

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="The chatbot took too long to respond. Please try again."
        )


    except Exception as e:
        print("GEMINI API ERROR:", repr(e))

        raise HTTPException(
        status_code=503,
        detail="Unable to connect to the AI service. Please check the backend terminal."
    )
