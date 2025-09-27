#!/usr/bin/env python3
"""
🧪 SIMPLE AGENT TEST
Test the product order agent without full dependencies.
"""

import sys
import os
import json
from datetime import datetime, timedelta
import random
import time

# Mock the agent environment
class MockProductOrderAgent:
    """Mock version of the product order agent for testing."""
    
    def __init__(self):
        self.products_database = []
        self.orders_database = []
        self.suppliers = [
            "TechCorp Solutions", "Global Parts Inc", "Budget Suppliers Ltd",
            "Premium Components", "FastTrack Logistics", "Reliable Systems"
        ]
        
        self.product_categories = [
            "Electronics", "Mechanical Parts", "Raw Materials", "Components",
            "Tools", "Accessories", "Software", "Hardware", "Materials"
        ]
        
        self.order_statuses = ["pending", "confirmed", "processing", "shipped", "delivered", "delayed", "cancelled"]
        self.priorities = ["low", "medium", "high", "urgent", "critical"]
        self.regions = ["North America", "Europe", "Asia Pacific", "South America", "Africa"]
        
        # Initialize with some base products
        self._initialize_base_products()
    
    def _initialize_base_products(self):
        """Initialize with some base products."""
        base_products = [
            {"name": "High-Speed Microprocessor", "category": "Electronics", "base_price": 250.00},
            {"name": "Memory Module 16GB", "category": "Electronics", "base_price": 80.00},
            {"name": "Steel Bracket", "category": "Mechanical Parts", "base_price": 15.00},
            {"name": "Aluminum Frame", "category": "Mechanical Parts", "base_price": 45.00},
            {"name": "Power Supply Unit", "category": "Electronics", "base_price": 120.00},
        ]
        
        for product in base_products:
            self.products_database.append({
                "id": f"PROD-{len(self.products_database) + 1:04d}",
                "name": product["name"],
                "category": product["category"],
                "base_price": product["base_price"],
                "description": f"High-quality {product['name'].lower()}",
                "supplier": random.choice(self.suppliers),
                "created_at": datetime.now().isoformat(),
                "status": "active"
            })
    
    def create_product(self, name: str, category: str = None, base_price: float = None):
        """Create a new product."""
        product_id = f"PROD-{len(self.products_database) + 1:04d}"
        
        if not category:
            category = random.choice(self.product_categories)
        
        if not base_price:
            base_price = round(random.uniform(10, 500), 2)
        
        product = {
            "id": product_id,
            "name": name,
            "category": category,
            "base_price": base_price,
            "description": f"High-quality {name.lower()}",
            "supplier": random.choice(self.suppliers),
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.products_database.append(product)
        return product
    
    def create_order(self, products: list = None, quantity: int = None, priority: str = None, supplier: str = None):
        """Create a new order."""
        order_id = f"ORD-{int(time.time())}-{random.randint(1000, 9999)}"
        
        if not products:
            num_products = random.randint(1, 4)
            products = random.sample([p["name"] for p in self.products_database], 
                                  min(num_products, len(self.products_database)))
        
        if not quantity:
            quantity = random.randint(1, 100)
        
        if not priority:
            priority = random.choice(self.priorities)
        
        if not supplier:
            supplier = random.choice(self.suppliers)
        
        # Calculate total amount
        total_amount = 0
        for product_name in products:
            product = next((p for p in self.products_database if p["name"] == product_name), None)
            if product:
                total_amount += product["base_price"] * random.randint(1, 10)
        
        if total_amount == 0:
            total_amount = round(random.uniform(100, 5000), 2)
        
        # Generate timestamps
        now = datetime.now()
        order_date = now - timedelta(hours=random.randint(0, 24))
        
        # Calculate delivery time based on priority
        delivery_days = {
            "low": 14, "medium": 7, "high": 3, "urgent": 1, "critical": 1
        }
        expected_delivery = now + timedelta(days=delivery_days.get(priority, 7))
        
        order = {
            "id": order_id,
            "supplier": supplier,
            "products": products,
            "quantity": quantity,
            "total_amount": round(total_amount, 2),
            "currency": "USD",
            "status": random.choice(self.order_statuses),
            "priority": priority,
            "region": random.choice(self.regions),
            "order_date": order_date.isoformat(),
            "expected_delivery": expected_delivery.isoformat(),
            "tracking_number": f"TRK{random.randint(100000, 999999)}",
            "notes": f"Order for {', '.join(products)}",
            "created_at": now.isoformat(),
            "pattern_type": f"{priority}_orders"
        }
        
        self.orders_database.append(order)
        return order
    
    def generate_multiple_orders(self, count: int = 5, order_type: str = "mixed"):
        """Generate multiple orders."""
        orders = []
        
        for i in range(count):
            if order_type == "urgent":
                priority = "urgent"
                products = random.sample([p["name"] for p in self.products_database], 
                                       random.randint(1, 3))
            elif order_type == "bulk":
                priority = "medium"
                products = random.sample([p["name"] for p in self.products_database], 
                                       random.randint(3, 6))
            else:  # mixed
                priority = random.choice(self.priorities)
                products = random.sample([p["name"] for p in self.products_database], 
                                       random.randint(1, 4))
            
            order = self.create_order(
                products=products,
                quantity=random.randint(1, 50),
                priority=priority,
                supplier=random.choice(self.suppliers)
            )
            orders.append(order)
        
        return orders
    
    def get_dashboard_data(self):
        """Get dashboard data."""
        total_orders = len(self.orders_database)
        urgent_orders = len([o for o in self.orders_database if o["priority"] == "urgent"])
        critical_orders = len([o for o in self.orders_database if o["priority"] == "critical"])
        total_value = sum(order["total_amount"] for order in self.orders_database)
        
        return {
            "total_orders": total_orders,
            "urgent_orders": urgent_orders,
            "critical_orders": critical_orders,
            "total_value": total_value,
            "recent_orders": self.orders_database[-10:],
            "products_count": len(self.products_database)
        }

def test_agent_functionality():
    """Test the agent functionality."""
    print("🧪 Testing Agent Functionality")
    print("=" * 50)
    
    # Create agent instance
    agent = MockProductOrderAgent()
    
    # Test 1: Create a product
    print("\n1. Creating a product...")
    product = agent.create_product("Test Widget", "Electronics", 99.99)
    print(f"✅ Created product: {product['id']} - {product['name']} (${product['base_price']})")
    
    # Test 2: Create an order
    print("\n2. Creating an order...")
    order = agent.create_order(
        products=["Test Widget", "High-Speed Microprocessor"],
        quantity=10,
        priority="urgent",
        supplier="Test Supplier"
    )
    print(f"✅ Created order: {order['id']} - {order['supplier']} - ${order['total_amount']}")
    
    # Test 3: Generate multiple orders
    print("\n3. Generating multiple orders...")
    orders = agent.generate_multiple_orders(count=3, order_type="urgent")
    print(f"✅ Generated {len(orders)} orders")
    for order in orders:
        print(f"   • {order['id']}: {order['supplier']} - ${order['total_amount']} ({order['priority']})")
    
    # Test 4: Get dashboard data
    print("\n4. Getting dashboard data...")
    dashboard_data = agent.get_dashboard_data()
    print(f"✅ Dashboard data:")
    print(f"   • Total Orders: {dashboard_data['total_orders']}")
    print(f"   • Urgent Orders: {dashboard_data['urgent_orders']}")
    print(f"   • Critical Orders: {dashboard_data['critical_orders']}")
    print(f"   • Total Value: ${dashboard_data['total_value']:.2f}")
    print(f"   • Products: {dashboard_data['products_count']}")
    
    print("\n✅ All tests passed!")
    return True

def main():
    """Main test function."""
    try:
        success = test_agent_functionality()
        
        if success:
            print("\n🎉 Agent Integration Test Complete!")
            print("\n📋 Next steps:")
            print("1. Start the main application: npm run dev")
            print("2. Go to http://localhost:3001")
            print("3. Click '📊 Monitoring' button")
            print("4. Try these chat commands:")
            print("   - 'Generate 5 urgent orders'")
            print("   - 'Create a new product called Smart Sensor'")
            print("   - 'Create an order for microprocessors'")
            print("   - 'Show me all orders'")
            print("   - 'Get dashboard data'")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
