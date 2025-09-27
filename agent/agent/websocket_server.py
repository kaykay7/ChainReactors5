"""
🌐 WEBSOCKET SERVER
Real-time communication between frontend and backend.
"""

import asyncio
import json
import websockets
from websockets.server import WebSocketServerProtocol
from typing import Dict, Any
import logging

from .streaming_orchestrator import StreamingAgentOrchestrator
from .mock_order_streamer import mock_order_streamer

class WebSocketServer:
    """WebSocket server for real-time communication."""
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.orchestrator = StreamingAgentOrchestrator()
        self.server = None
        self.clients: Dict[str, WebSocketServerProtocol] = {}
        
    async def start_server(self):
        """Start the WebSocket server."""
        await self.orchestrator.start_streaming()
        
        # Start mock order streaming in background
        asyncio.create_task(mock_order_streamer.start_streaming())
        
        self.server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        
        print(f"🌐 WebSocket server started on ws://{self.host}:{self.port}")
        print(f"📦 Mock order streaming started")
        
        # Keep the server running
        await self.server.wait_closed()
    
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle a new client connection."""
        client_id = f"client_{id(websocket)}"
        self.clients[client_id] = websocket
        
        await self.orchestrator.add_client(websocket)
        await mock_order_streamer.add_client(websocket)
        
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.orchestrator.remove_client(websocket)
            await mock_order_streamer.remove_client(websocket)
            if client_id in self.clients:
                del self.clients[client_id]
    
    async def handle_message(self, websocket: WebSocketServerProtocol, message: str):
        """Handle incoming messages from clients."""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "user_request":
                await self.handle_user_request(websocket, data)
            elif message_type == "ping":
                await websocket.send(json.dumps({"type": "pong"}))
            else:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": f"Unknown message type: {message_type}"
                }))
                
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "type": "error",
                "message": "Invalid JSON format"
            }))
        except Exception as e:
            await websocket.send(json.dumps({
                "type": "error",
                "message": f"Server error: {str(e)}"
            }))
    
    async def handle_user_request(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Handle user requests with streaming responses."""
        user_input = data.get("user_input", "")
        context = data.get("context", {})
        user_id = data.get("user_id")
        
        try:
            # Stream the response
            async for response in self.orchestrator.stream_user_request(user_input, context, user_id):
                await websocket.send(json.dumps(response))
        except Exception as e:
            await websocket.send(json.dumps({
                "type": "error",
                "message": f"Processing error: {str(e)}"
            }))

# Server startup
async def main():
    server = WebSocketServer()
    await server.start_server()

if __name__ == "__main__":
    asyncio.run(main())
