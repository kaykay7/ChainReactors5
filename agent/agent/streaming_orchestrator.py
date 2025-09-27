"""
🔄 STREAMING AGENT ORCHESTRATOR
Real-time coordination with streaming responses and live updates.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, AsyncGenerator
from datetime import datetime
from dataclasses import dataclass
import websockets
from websockets.server import WebSocketServerProtocol

from .agent_orchestrator import AgentOrchestrator
from .memory_manager import AgentMemoryManager
from .csv_data_source import CSVDataSource

@dataclass
class StreamingEvent:
    """Event structure for streaming updates."""
    event_type: str  # "item_added", "item_removed", "item_updated", "field_changed"
    item_id: str
    data: Dict[str, Any]
    timestamp: datetime
    agent_id: str
    user_id: Optional[str] = None

class StreamingAgentOrchestrator(AgentOrchestrator):
    """Enhanced orchestrator with streaming capabilities."""
    
    def __init__(self, memory_dir: str = "./agent_memory", csv_dir: str = "./mock_data"):
        super().__init__(memory_dir, csv_dir)
        self.connected_clients: List[WebSocketServerProtocol] = []
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self.streaming_active = False
        
    async def start_streaming(self):
        """Start the streaming service."""
        self.streaming_active = True
        asyncio.create_task(self._process_event_queue())
        print("🔄 Streaming service started")
    
    async def stop_streaming(self):
        """Stop the streaming service."""
        self.streaming_active = False
        print("🔄 Streaming service stopped")
    
    async def add_client(self, websocket: WebSocketServerProtocol):
        """Add a new client to the streaming service."""
        self.connected_clients.append(websocket)
        print(f"📡 Client connected. Total clients: {len(self.connected_clients)}")
    
    async def remove_client(self, websocket: WebSocketServerProtocol):
        """Remove a client from the streaming service."""
        if websocket in self.connected_clients:
            self.connected_clients.remove(websocket)
        print(f"📡 Client disconnected. Total clients: {len(self.connected_clients)}")
    
    async def broadcast_event(self, event: StreamingEvent):
        """Broadcast an event to all connected clients."""
        if not self.connected_clients:
            return
        
        event_data = {
            "event_type": event.event_type,
            "item_id": event.item_id,
            "data": event.data,
            "timestamp": event.timestamp.isoformat(),
            "agent_id": event.agent_id,
            "user_id": event.user_id
        }
        
        # Send to all connected clients
        disconnected_clients = []
        for client in self.connected_clients:
            try:
                await client.send(json.dumps(event_data))
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            await self.remove_client(client)
    
    async def _process_event_queue(self):
        """Process events from the queue and broadcast them."""
        while self.streaming_active:
            try:
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                await self.broadcast_event(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"❌ Error processing event: {e}")
    
    async def stream_user_request(self, user_input: str, context: Dict[str, Any], 
                                user_id: Optional[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Process user request with streaming responses."""
        
        # Start with initial response
        yield {
            "type": "start",
            "message": "Processing your request...",
            "timestamp": datetime.now().isoformat()
        }
        
        # Analyze intent and determine required agents
        intent = await self._analyze_intent(user_input)
        yield {
            "type": "intent_analysis",
            "intent": intent,
            "message": f"Detected intent: {intent['primary_intent']}",
            "timestamp": datetime.now().isoformat()
        }
        
        # Process with appropriate agents
        if intent["primary_intent"] == "inventory_management":
            async for response in self._stream_inventory_operations(user_input, context, user_id):
                yield response
        elif intent["primary_intent"] == "supplier_management":
            async for response in self._stream_supplier_operations(user_input, context, user_id):
                yield response
        elif intent["primary_intent"] == "forecasting":
            async for response in self._stream_forecasting_operations(user_input, context, user_id):
                yield response
        else:
            # General orchestration
            async for response in self._stream_general_operations(user_input, context, user_id):
                yield response
    
    async def _stream_inventory_operations(self, user_input: str, context: Dict[str, Any], 
                                         user_id: Optional[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream inventory-related operations."""
        
        # Get inventory agent
        inventory_agent = self.agents["inventory_agent"]
        
        # Analyze current inventory
        yield {
            "type": "inventory_analysis",
            "message": "Analyzing current inventory levels...",
            "timestamp": datetime.now().isoformat()
        }
        
        analysis = await inventory_agent.analyze_stock_levels(context.get("inventory_data"))
        
        # Stream analysis results
        yield {
            "type": "analysis_results",
            "data": analysis,
            "message": f"Found {len(analysis.get('low_stock_items', []))} low stock items",
            "timestamp": datetime.now().isoformat()
        }
        
        # Check for items that need to be added/removed
        if "add" in user_input.lower() or "create" in user_input.lower():
            # Stream item creation
            yield {
                "type": "item_creation",
                "message": "Creating new inventory items...",
                "timestamp": datetime.now().isoformat()
            }
            
            # Simulate item creation with streaming updates
            new_items = await self._create_inventory_items(analysis, user_input)
            for item in new_items:
                event = StreamingEvent(
                    event_type="item_added",
                    item_id=item["id"],
                    data=item,
                    timestamp=datetime.now(),
                    agent_id="inventory_agent",
                    user_id=user_id
                )
                await self.event_queue.put(event)
                
                yield {
                    "type": "item_added",
                    "item_id": item["id"],
                    "data": item,
                    "message": f"Added item: {item['name']}",
                    "timestamp": datetime.now().isoformat()
                }
        
        if "remove" in user_input.lower() or "delete" in user_input.lower():
            # Stream item removal
            yield {
                "type": "item_removal",
                "message": "Removing inventory items...",
                "timestamp": datetime.now().isoformat()
            }
            
            # Simulate item removal with streaming updates
            items_to_remove = await self._identify_items_to_remove(analysis, user_input)
            for item_id in items_to_remove:
                event = StreamingEvent(
                    event_type="item_removed",
                    item_id=item_id,
                    data={"reason": "User requested removal"},
                    timestamp=datetime.now(),
                    agent_id="inventory_agent",
                    user_id=user_id
                )
                await self.event_queue.put(event)
                
                yield {
                    "type": "item_removed",
                    "item_id": item_id,
                    "message": f"Removed item: {item_id}",
                    "timestamp": datetime.now().isoformat()
                }
    
    async def _create_inventory_items(self, analysis: Dict[str, Any], user_input: str) -> List[Dict[str, Any]]:
        """Create new inventory items based on analysis."""
        # Simulate item creation
        items = []
        for i in range(3):  # Create 3 sample items
            item = {
                "id": f"item_{datetime.now().timestamp()}_{i}",
                "name": f"New Product {i+1}",
                "type": "inventory",
                "current_stock": 0,
                "min_stock": 10,
                "max_stock": 100,
                "reorder_point": 20,
                "supplier": "TechCorp Solutions",
                "created_at": datetime.now().isoformat()
            }
            items.append(item)
        return items
    
    async def _identify_items_to_remove(self, analysis: Dict[str, Any], user_input: str) -> List[str]:
        """Identify items to remove based on analysis."""
        # Simulate item identification for removal
        return [f"item_to_remove_{i}" for i in range(2)]  # Remove 2 sample items
    
    async def _stream_supplier_operations(self, user_input: str, context: Dict[str, Any], 
                                        user_id: Optional[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream supplier-related operations."""
        supplier_agent = self.agents["supplier_agent"]
        
        yield {
            "type": "supplier_analysis",
            "message": "Analyzing supplier performance...",
            "timestamp": datetime.now().isoformat()
        }
        
        # Stream supplier analysis
        analysis = await supplier_agent.analyze_supplier_performance(context.get("supplier_data"))
        
        yield {
            "type": "supplier_results",
            "data": analysis,
            "message": "Supplier analysis completed",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _stream_forecasting_operations(self, user_input: str, context: Dict[str, Any], 
                                           user_id: Optional[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream forecasting operations."""
        forecasting_agent = self.agents["forecasting_agent"]
        
        yield {
            "type": "forecasting_analysis",
            "message": "Running demand forecasting...",
            "timestamp": datetime.now().isoformat()
        }
        
        # Stream forecasting results
        forecast = await forecasting_agent.forecast_demand(context.get("historical_data"))
        
        yield {
            "type": "forecast_results",
            "data": forecast,
            "message": "Demand forecast completed",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _stream_general_operations(self, user_input: str, context: Dict[str, Any], 
                                       user_id: Optional[str] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream general operations."""
        yield {
            "type": "general_processing",
            "message": "Processing your request...",
            "timestamp": datetime.now().isoformat()
        }
        
        # Simulate general processing
        await asyncio.sleep(1)  # Simulate processing time
        
        yield {
            "type": "general_complete",
            "message": "Request processed successfully",
            "timestamp": datetime.now().isoformat()
        }
