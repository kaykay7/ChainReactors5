"""
🏪 AMAZON DASHBOARD SERVER
FastAPI server with WebSocket support for Amazon-style supply chain monitoring.
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from typing import Dict, List
import uvicorn

from .amazon_style_monitor import AmazonStyleMonitor

app = FastAPI(title="Amazon-Style Supply Chain Dashboard")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global monitor instance
monitor = AmazonStyleMonitor()

@app.on_event("startup")
async def startup_event():
    """Start the monitoring service."""
    await monitor.start_monitoring()
    print("🏪 Amazon-style monitoring started")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the monitoring service."""
    await monitor.stop_monitoring()
    print("🏪 Monitoring stopped")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    await websocket.accept()
    await monitor.add_subscriber(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "get_dashboard_data":
                # Send current dashboard data
                dashboard_data = await monitor.get_dashboard_data()
                await websocket.send_text(json.dumps({
                    "type": "dashboard_data",
                    "data": dashboard_data
                }))
            
            elif message.get("type") == "acknowledge_alert":
                alert_id = message.get("alert_id")
                success = await monitor.acknowledge_alert(alert_id)
                await websocket.send_text(json.dumps({
                    "type": "alert_acknowledged",
                    "alert_id": alert_id,
                    "success": success
                }))
            
            elif message.get("type") == "resolve_alert":
                alert_id = message.get("alert_id")
                success = await monitor.resolve_alert(alert_id)
                await websocket.send_text(json.dumps({
                    "type": "alert_resolved",
                    "alert_id": alert_id,
                    "success": success
                }))
            
            elif message.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
                
    except WebSocketDisconnect:
        await monitor.remove_subscriber(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

@app.get("/api/dashboard")
async def get_dashboard():
    """Get current dashboard data."""
    return await monitor.get_dashboard_data()

@app.post("/api/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    """Acknowledge an alert."""
    success = await monitor.acknowledge_alert(alert_id)
    return {"success": success, "alert_id": alert_id}

@app.post("/api/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str):
    """Resolve an alert."""
    success = await monitor.resolve_alert(alert_id)
    return {"success": success, "alert_id": alert_id}

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "monitoring_active": monitor.monitoring_active,
        "active_alerts": len(monitor.active_alerts),
        "subscribers": len(monitor.subscribers)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)
