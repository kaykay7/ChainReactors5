#!/usr/bin/env python3
"""
🧪 SIMPLE MOCK ORDER TEST
Simple test to verify mock order generation without dependencies.
"""

import asyncio
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any

class SimpleMockOrderGenerator:
    """Simple mock order generator for testing."""
    
    def __init__(self):
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
        
        self.order_patterns = {
            "rush_orders": {"frequency": 0.1, "priority": "urgent", "delivery_time": 1},
            "bulk_orders": {"frequency": 0.15, "priority": "medium", "delivery_time": 7},
            "regular_orders": {"frequency": 0.6, "priority": "medium", "delivery_time": 3},
            "premium_orders": {"frequency": 0.1, "priority": "high", "delivery_time": 2},
            "delayed_orders": {"frequency": 0.05, "priority": "low", "delivery_time": 14}
        }
    
    async def generate_mock_order(self) -> Dict[str, Any]:
        """Generate a single mock order."""
        pattern = self.select_order_pattern()
        
        order_id = f"ORD-{int(time.time())}-{random.randint(1000, 9999)}"
        supplier = random.choice(self.suppliers)
        product_count = random.randint(1, 5)
        products = random.sample(self.products, product_count)
        
        base_amount = random.uniform(100, 5000)
        if pattern["priority"] == "urgent":
            base_amount *= 1.5
        elif pattern["priority"] == "low":
            base_amount *= 0.7
        
        total_amount = round(base_amount, 2)
        
        now = datetime.now()
        order_date = now - timedelta(hours=random.randint(0, 24))
        expected_delivery = now + timedelta(days=pattern["delivery_time"])
        
        if random.random() < 0.1:
            expected_delivery += timedelta(days=random.randint(1, 7))
        
        return {
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
        
        return {
            "type": "regular_orders",
            "priority": "medium",
            "delivery_time": 3
        }
    
    def generate_order_notes(self, pattern: Dict[str, Any]) -> str:
        """Generate realistic order notes."""
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

async def test_mock_orders():
    """Test mock order generation."""
    print("🧪 Testing mock order generation...")
    print("=" * 50)
    
    generator = SimpleMockOrderGenerator()
    
    # Generate test orders
    for i in range(10):
        order = await generator.generate_mock_order()
        print(f"\n📦 Order {i+1}:")
        print(f"   ID: {order['id']}")
        print(f"   Supplier: {order['supplier']}")
        print(f"   Products: {', '.join(order['products'])}")
        print(f"   Amount: ${order['total_amount']}")
        print(f"   Status: {order['status']}")
        print(f"   Priority: {order['priority']}")
        print(f"   Pattern: {order['pattern_type']}")
        print(f"   Notes: {order['notes']}")
        print(f"   Region: {order['region']}")
    
    print("\n✅ Mock order generation test completed!")
    print("\n📋 To start real streaming:")
    print("1. Run: python3 start_mock_streaming.py")
    print("2. Open monitoring dashboard")
    print("3. Watch real-time order data!")

if __name__ == "__main__":
    asyncio.run(test_mock_orders())
