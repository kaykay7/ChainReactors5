#!/usr/bin/env python3
"""
🚀 STREAMING SERVER STARTUP
Start the streaming server with WebSocket support.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the agent directory to Python path
agent_dir = Path(__file__).parent / "agent"
sys.path.insert(0, str(agent_dir))

from agent.streaming_server import app
import uvicorn

def main():
    """Start the streaming server."""
    print("🚀 Starting Streaming Server...")
    print("📡 WebSocket endpoint: ws://localhost:8765")
    print("🌐 HTTP endpoint: http://localhost:9000")
    print("🔄 Streaming enabled for real-time updates")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9000,
        log_level="info",
        reload=False
    )

if __name__ == "__main__":
    main()
