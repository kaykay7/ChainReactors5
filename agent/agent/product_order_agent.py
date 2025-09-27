"""
🤖 PRODUCT & ORDER GENERATION AGENT
Agent responsible for creating products and orders from chat commands.
"""

import asyncio
import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductOrderAgent:
    """Agent that generates products and orders based on chat commands."""
    
    def __init__(self):
        self.products_database = []
        self.orders_database = []
        self.suppliers = [
            "TechCorp Solutions", "Global Parts Inc", "Budget Suppliers Ltd",
            "Premium Components", "FastTrack Logistics", "Reliable Systems",
            "Innovation Labs", "Quality Materials Co", "Express Suppliers"
        ]
        
        self.product_categories = [
            "Electronics", "Mechanical Parts", "Raw Materials", "Components",
            "Tools", "Accessories", "Software", "Hardware", "Materials"
        ]
        
        self.product_types = [
            "Microprocessors", "Memory chips", "Circuit boards", "Steel components",
            "Aluminum parts", "Plastic materials", "Electronic sensors",
            "Power supplies", "Cables", "Connectors", "Sensors", "Actuators",
            "Controllers", "Displays", "Keyboards", "Mouse", "Monitors"
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
            {"name": "Data Cable", "category": "Accessories", "base_price": 25.00},
            {"name": "Sensor Module", "category": "Electronics", "base_price": 65.00},
            {"name": "Control Board", "category": "Electronics", "base_price": 180.00},
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
    
    def create_product(self, name: str, category: str = None, base_price: float = None) -> Dict[str, Any]:
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
        logger.info(f"Created product: {product_id} - {name}")
        return product
    
    def create_order(self, 
                    products: List[str] = None, 
                    quantity: int = None,
                    priority: str = None,
                    supplier: str = None,
                    customer_notes: str = None) -> Dict[str, Any]:
        """Create a new order."""
        order_id = f"ORD-{int(time.time())}-{random.randint(1000, 9999)}"
        
        if not products:
            # Select random products from database
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
            "notes": customer_notes or f"Order for {', '.join(products)}",
            "created_at": now.isoformat(),
            "pattern_type": f"{priority}_orders"
        }
        
        self.orders_database.append(order)
        logger.info(f"Created order: {order_id} - {supplier} - ${total_amount}")
        return order
    
    def generate_multiple_orders(self, count: int = 5, order_type: str = "mixed") -> List[Dict[str, Any]]:
        """Generate multiple orders based on type."""
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
            elif order_type == "premium":
                priority = "high"
                products = random.sample([p["name"] for p in self.products_database], 
                                       random.randint(1, 2))
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
    
    def get_products(self) -> List[Dict[str, Any]]:
        """Get all products."""
        return self.products_database
    
    def get_orders(self) -> List[Dict[str, Any]]:
        """Get all orders."""
        return self.orders_database
    
    def get_orders_by_priority(self, priority: str) -> List[Dict[str, Any]]:
        """Get orders by priority."""
        return [order for order in self.orders_database if order["priority"] == priority]
    
    def get_orders_by_supplier(self, supplier: str) -> List[Dict[str, Any]]:
        """Get orders by supplier."""
        return [order for order in self.orders_database if order["supplier"] == supplier]
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Search products by name or category."""
        query_lower = query.lower()
        return [product for product in self.products_database 
                if query_lower in product["name"].lower() or 
                   query_lower in product["category"].lower()]
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for dashboard display."""
        total_orders = len(self.orders_database)
        urgent_orders = len([o for o in self.orders_database if o["priority"] == "urgent"])
        critical_orders = len([o for o in self.orders_database if o["priority"] == "critical"])
        total_value = sum(order["total_amount"] for order in self.orders_database)
        
        return {
            "total_orders": total_orders,
            "urgent_orders": urgent_orders,
            "critical_orders": critical_orders,
            "total_value": total_value,
            "recent_orders": self.orders_database[-10:],  # Last 10 orders
            "products_count": len(self.products_database)
        }

# Global agent instance
product_order_agent = ProductOrderAgent()

def create_product_command(name: str, category: str = None, base_price: float = None) -> str:
    """Command to create a product."""
    product = product_order_agent.create_product(name, category, base_price)
    return f"✅ Created product: {product['id']} - {product['name']} (${product['base_price']})"

def create_order_command(products: List[str] = None, quantity: int = None, 
                        priority: str = None, supplier: str = None) -> str:
    """Command to create an order."""
    order = product_order_agent.create_order(products, quantity, priority, supplier)
    return f"✅ Created order: {order['id']} - {order['supplier']} - ${order['total_amount']}"

def generate_orders_command(count: int = 5, order_type: str = "mixed") -> str:
    """Command to generate multiple orders."""
    orders = product_order_agent.generate_multiple_orders(count, order_type)
    total_value = sum(order["total_amount"] for order in orders)
    return f"✅ Generated {len(orders)} orders (Total value: ${total_value:.2f})"

def get_products_command() -> str:
    """Command to get all products."""
    products = product_order_agent.get_products()
    if not products:
        return "No products found."
    
    product_list = "\n".join([f"• {p['id']}: {p['name']} (${p['base_price']})" for p in products])
    return f"📦 Products ({len(products)}):\n{product_list}"

def get_orders_command() -> str:
    """Command to get all orders."""
    orders = product_order_agent.get_orders()
    if not orders:
        return "No orders found."
    
    order_list = "\n".join([f"• {o['id']}: {o['supplier']} - ${o['total_amount']} ({o['priority']})" for o in orders[-10:]])
    return f"📋 Recent Orders ({len(orders)}):\n{order_list}"

def get_dashboard_data_command() -> str:
    """Command to get dashboard data."""
    data = product_order_agent.get_dashboard_data()
    return f"""📊 Dashboard Data:
• Total Orders: {data['total_orders']}
• Urgent Orders: {data['urgent_orders']}
• Critical Orders: {data['critical_orders']}
• Total Value: ${data['total_value']:.2f}
• Products: {data['products_count']}"""

# Export functions for use in other modules
__all__ = [
    'product_order_agent',
    'create_product_command',
    'create_order_command', 
    'generate_orders_command',
    'get_products_command',
    'get_orders_command',
    'get_dashboard_data_command'
]
