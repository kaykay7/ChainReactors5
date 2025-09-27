#!/usr/bin/env python3
"""
🚀 START MOCK ORDER STREAMING
Starts the WebSocket server with mock order streaming for testing monitoring dashboard.
"""

import asyncio
import sys
import os

# Add the agent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.websocket_server import WebSocketServer

async def main():
    """Start the WebSocket server with mock order streaming."""
    print("🚀 Starting WebSocket server with mock order streaming...")
    print("📦 This will generate realistic order data with variations")
    print("🌐 Connect to ws://localhost:8765 to receive order updates")
    print("📊 Use the monitoring dashboard to see real-time order data")
    print("=" * 60)
    
    server = WebSocketServer(host="localhost", port=8765)
    
    try:
        await server.start_server()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        print("✅ Server stopped")

if __name__ == "__main__":
    asyncio.run(main())
