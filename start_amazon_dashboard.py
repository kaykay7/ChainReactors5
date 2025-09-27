#!/usr/bin/env python3
"""
🏪 AMAZON DASHBOARD STARTUP
Start the Amazon-style supply chain monitoring dashboard.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the agent directory to Python path
agent_dir = Path(__file__).parent / "agent"
sys.path.insert(0, str(agent_dir))

from agent.amazon_dashboard_server import app
import uvicorn

def main():
    """Start the Amazon-style dashboard server."""
    print("🏪 Starting Amazon-Style Supply Chain Dashboard...")
    print("📡 WebSocket endpoint: ws://localhost:8765")
    print("🌐 HTTP endpoint: http://localhost:9001")
    print("🔄 Real-time monitoring enabled for:")
    print("   • Low stock alerts")
    print("   • Shipping delays")
    print("   • Supplier issues")
    print("   • Demand surges")
    print("   • Price changes")
    print("   • Quality issues")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9001,
        log_level="info",
        reload=False
    )

if __name__ == "__main__":
    main()
