"""
🚀 STREAMING SERVER
FastAPI server with WebSocket support for real-time streaming.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from typing import Dict, List
import uvicorn

from .streaming_orchestrator import StreamingAgentOrchestrator

app = FastAPI(title="Streaming Agent Server")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator = StreamingAgentOrchestrator()

@app.on_event("startup")
async def startup_event():
    """Start the streaming service."""
    await orchestrator.start_streaming()
    print("🚀 Streaming server started")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the streaming service."""
    await orchestrator.stop_streaming()
    print("🚀 Streaming server stopped")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    await websocket.accept()
    await orchestrator.add_client(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "user_request":
                # Stream the response
                async for response in orchestrator.stream_user_request(
                    message.get("user_input", ""),
                    message.get("context", {}),
                    message.get("user_id")
                ):
                    await websocket.send_text(json.dumps(response))
            
            elif message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
                
    except WebSocketDisconnect:
        await orchestrator.remove_client(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

@app.post("/api/streaming/request")
async def streaming_request(request: Dict):
    """HTTP endpoint for streaming requests."""
    user_input = request.get("user_input", "")
    context = request.get("context", {})
    user_id = request.get("user_id")
    
    # Process with streaming
    responses = []
    async for response in orchestrator.stream_user_request(user_input, context, user_id):
        responses.append(response)
    
    return {"responses": responses}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
