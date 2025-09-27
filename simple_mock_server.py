#!/usr/bin/env python3
"""
🌐 SIMPLE MOCK ORDER SERVER
HTTP server for streaming mock orders without WebSocket dependencies.
"""

import asyncio
import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockOrderGenerator:
    """Generates realistic mock orders."""
    
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
    
    def generate_mock_order(self) -> Dict[str, Any]:
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

class MockOrderHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mock order API."""
    
    def __init__(self, *args, **kwargs):
        self.generator = MockOrderGenerator()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == "/api/orders":
            self.handle_get_orders()
        elif path == "/api/orders/batch":
            self.handle_get_batch()
        elif path == "/":
            self.handle_root()
        else:
            self.send_error(404, "Not Found")
    
    def handle_root(self):
        """Handle root path - return API documentation."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Mock Order API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
                code { background: #e8e8e8; padding: 2px 4px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>📦 Mock Order API</h1>
            <p>This server generates realistic mock orders for testing the monitoring dashboard.</p>
            
            <h2>Available Endpoints:</h2>
            
            <div class="endpoint">
                <h3>GET /api/orders</h3>
                <p>Generate a single random order</p>
                <p><code>curl http://localhost:8765/api/orders</code></p>
            </div>
            
            <div class="endpoint">
                <h3>GET /api/orders/batch</h3>
                <p>Generate a batch of 1-3 random orders</p>
                <p><code>curl http://localhost:8765/api/orders/batch</code></p>
            </div>
            
            <h2>Order Patterns:</h2>
            <ul>
                <li><strong>Rush Orders (10%)</strong>: Urgent priority, 1-day delivery</li>
                <li><strong>Bulk Orders (15%)</strong>: Medium priority, 7-day delivery</li>
                <li><strong>Regular Orders (60%)</strong>: Medium priority, 3-day delivery</li>
                <li><strong>Premium Orders (10%)</strong>: High priority, 2-day delivery</li>
                <li><strong>Delayed Orders (5%)</strong>: Low priority, 14-day delivery</li>
            </ul>
            
            <h2>Usage:</h2>
            <p>Use these endpoints in your monitoring dashboard to fetch mock order data.</p>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode())
    
    def handle_get_orders(self):
        """Handle single order request."""
        try:
            order = self.generator.generate_mock_order()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "success": True,
                "data": order,
                "timestamp": datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def handle_get_batch(self):
        """Handle batch order request."""
        try:
            batch_size = random.randint(1, 3)
            orders = []
            
            for _ in range(batch_size):
                order = self.generator.generate_mock_order()
                orders.append(order)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "success": True,
                "data": {
                    "orders": orders,
                    "batch_size": len(orders),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def log_message(self, format, *args):
        """Override to reduce log noise."""
        pass

def start_server(port=8765):
    """Start the mock order server."""
    print("🚀 Starting Simple Mock Order Server...")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"📦 API: http://localhost:{port}/api/orders")
    print(f"📦 Batch: http://localhost:{port}/api/orders/batch")
    print("=" * 50)
    
    try:
        server = HTTPServer(('localhost', port), MockOrderHandler)
        print(f"✅ Server started on http://localhost:{port}")
        print("📋 Available endpoints:")
        print(f"   • http://localhost:{port}/api/orders")
        print(f"   • http://localhost:{port}/api/orders/batch")
        print("\n🛑 Press Ctrl+C to stop")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server.shutdown()
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        print("✅ Server stopped")

if __name__ == "__main__":
    start_server()
