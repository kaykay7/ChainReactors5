"""
📦 MOCK ORDER STREAMER
Generates realistic order data with variations for testing monitoring dashboard.
"""

import asyncio
import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

class MockOrderStreamer:
    """Streams realistic mock order data with variations."""
    
    def __init__(self):
        self.running = False
        self.clients = []
        
        # Mock data templates
        self.suppliers = [
            "TechCorp Solutions", "Global Parts Inc", "Budget Suppliers Ltd",
            "Premium Components", "FastTrack Logistics", "Reliable Systems"
        ]
        
        self.products = [
            "Microprocessors", "Memory chips", "Circuit boards", "Steel components",
            "Aluminum parts", "Plastic materials", "Electronic sensors",
            "Power supplies", "Cables", "Connectors"
        ]
        
        self.statuses = ["pending", "confirmed", "processing", "shipped", "delivered", "delayed", "cancelled"]
        self.priorities = ["low", "medium", "high", "urgent", "critical"]
        self.regions = ["North America", "Europe", "Asia Pacific", "South America", "Africa"]
        
        # Order patterns for realistic variations
        self.order_patterns = {
            "rush_orders": {"frequency": 0.1, "priority": "urgent", "delivery_time": 1},
            "bulk_orders": {"frequency": 0.15, "priority": "medium", "delivery_time": 7},
            "regular_orders": {"frequency": 0.6, "priority": "medium", "delivery_time": 3},
            "premium_orders": {"frequency": 0.1, "priority": "high", "delivery_time": 2},
            "delayed_orders": {"frequency": 0.05, "priority": "low", "delivery_time": 14}
        }
    
    async def start_streaming(self):
        """Start streaming mock orders."""
        self.running = True
        print("📦 Starting mock order streaming...")
        
        while self.running:
            try:
                # Generate a batch of orders (1-3 orders per batch)
                batch_size = random.randint(1, 3)
                orders = []
                
                for _ in range(batch_size):
                    order = await self.generate_mock_order()
                    orders.append(order)
                
                # Send to all connected clients
                await self.broadcast_orders(orders)
                
                # Wait between batches (2-8 seconds)
                await asyncio.sleep(random.uniform(2, 8))
                
            except Exception as e:
                logging.error(f"Error in order streaming: {e}")
                await asyncio.sleep(5)
    
    async def generate_mock_order(self) -> Dict[str, Any]:
        """Generate a single mock order with realistic variations."""
        # Determine order pattern
        pattern = self.select_order_pattern()
        
        # Generate order data
        order_id = f"ORD-{int(time.time())}-{random.randint(1000, 9999)}"
        supplier = random.choice(self.suppliers)
        product_count = random.randint(1, 5)
        products = random.sample(self.products, product_count)
        
        # Calculate realistic amounts
        base_amount = random.uniform(100, 5000)
        if pattern["priority"] == "urgent":
            base_amount *= 1.5  # Rush orders cost more
        elif pattern["priority"] == "low":
            base_amount *= 0.7  # Bulk orders cost less
        
        total_amount = round(base_amount, 2)
        
        # Generate timestamps
        now = datetime.now()
        order_date = now - timedelta(hours=random.randint(0, 24))
        expected_delivery = now + timedelta(days=pattern["delivery_time"])
        
        # Add some randomness to delivery times
        if random.random() < 0.1:  # 10% chance of delay
            expected_delivery += timedelta(days=random.randint(1, 7))
        
        order = {
            "id": order_id,
            "supplier": supplier,
            "products": products,
            "quantity": random.randint(1, 100),
            "total_amount": total_amount,
            "currency": "USD",
            "status": random.choice(self.statuses),
            "priority": pattern["priority"],
            "region": random.choice(self.regions),
            "order_date": order_date.isoformat(),
            "expected_delivery": expected_delivery.isoformat(),
            "tracking_number": f"TRK{random.randint(100000, 999999)}",
            "notes": self.generate_order_notes(pattern),
            "created_at": now.isoformat(),
            "pattern_type": pattern["type"]
        }
        
        return order
    
    def select_order_pattern(self) -> Dict[str, Any]:
        """Select an order pattern based on frequency."""
        rand = random.random()
        cumulative = 0
        
        for pattern_name, pattern_data in self.order_patterns.items():
            cumulative += pattern_data["frequency"]
            if rand <= cumulative:
                return {
                    "type": pattern_name,
                    "priority": pattern_data["priority"],
                    "delivery_time": pattern_data["delivery_time"]
                }
        
        # Fallback to regular orders
        return {
            "type": "regular_orders",
            "priority": "medium",
            "delivery_time": 3
        }
    
    def generate_order_notes(self, pattern: Dict[str, Any]) -> str:
        """Generate realistic order notes based on pattern."""
        notes_templates = {
            "rush_orders": [
                "Express delivery required",
                "Customer emergency order",
                "Expedited processing needed",
                "Rush shipment requested"
            ],
            "bulk_orders": [
                "Volume discount applied",
                "Bulk shipment processing",
                "Large quantity order",
                "Wholesale pricing"
            ],
            "regular_orders": [
                "Standard processing",
                "Normal delivery timeline",
                "Regular order processing",
                "Standard shipment"
            ],
            "premium_orders": [
                "Premium service requested",
                "High-priority customer",
                "VIP processing",
                "Premium delivery"
            ],
            "delayed_orders": [
                "Backorder processing",
                "Delayed shipment",
                "Inventory shortage",
                "Extended lead time"
            ]
        }
        
        return random.choice(notes_templates.get(pattern["type"], ["Standard order"]))
    
    async def broadcast_orders(self, orders: List[Dict[str, Any]]):
        """Broadcast orders to all connected clients."""
        if not self.clients:
            return
        
        message = {
            "type": "mock_orders",
            "data": {
                "orders": orders,
                "timestamp": datetime.now().isoformat(),
                "batch_size": len(orders)
            }
        }
        
        # Send to all clients
        disconnected_clients = []
        for client in self.clients:
            try:
                await client.send(json.dumps(message))
            except Exception as e:
                logging.warning(f"Failed to send to client: {e}")
                disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            if client in self.clients:
                self.clients.remove(client)
    
    async def add_client(self, websocket):
        """Add a new client to receive order updates."""
        self.clients.append(websocket)
        print(f"📦 Client connected to order streamer. Total clients: {len(self.clients)}")
    
    async def remove_client(self, websocket):
        """Remove a client from order updates."""
        if websocket in self.clients:
            self.clients.remove(websocket)
        print(f"📦 Client disconnected from order streamer. Total clients: {len(self.clients)}")
    
    async def stop_streaming(self):
        """Stop streaming orders."""
        self.running = False
        print("📦 Stopping mock order streaming...")

# Global instance
mock_order_streamer = MockOrderStreamer()

async def start_mock_order_streaming():
    """Start the mock order streaming service."""
    await mock_order_streamer.start_streaming()

if __name__ == "__main__":
    asyncio.run(start_mock_order_streaming())
