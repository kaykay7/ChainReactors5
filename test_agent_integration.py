#!/usr/bin/env python3
"""
🧪 TEST AGENT INTEGRATION
Test the product order agent integration.
"""

import sys
import os

# Add the agent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'agent')))

from agent.product_order_agent import (
    product_order_agent,
    create_product_command,
    create_order_command,
    generate_orders_command,
    get_products_command,
    get_orders_command,
    get_dashboard_data_command
)

def test_product_creation():
    """Test product creation."""
    print("🧪 Testing product creation...")
    
    # Create a test product
    result = create_product_command("Test Widget", "Electronics", 99.99)
    print(f"✅ {result}")
    
    # Get products
    products = get_products_command()
    print(f"📦 Products: {products}")

def test_order_creation():
    """Test order creation."""
    print("\n🧪 Testing order creation...")
    
    # Create a test order
    result = create_order_command(
        products=["Test Widget", "High-Speed Microprocessor"],
        quantity=10,
        priority="urgent",
        supplier="Test Supplier"
    )
    print(f"✅ {result}")
    
    # Get orders
    orders = get_orders_command()
    print(f"📋 Orders: {orders}")

def test_bulk_order_generation():
    """Test bulk order generation."""
    print("\n🧪 Testing bulk order generation...")
    
    # Generate multiple orders
    result = generate_orders_command(count=3, order_type="urgent")
    print(f"✅ {result}")
    
    # Get dashboard data
    dashboard_data = get_dashboard_data_command()
    print(f"📊 Dashboard: {dashboard_data}")

def test_agent_integration():
    """Test the complete agent integration."""
    print("🚀 Testing Agent Integration")
    print("=" * 50)
    
    try:
        # Test product creation
        test_product_creation()
        
        # Test order creation
        test_order_creation()
        
        # Test bulk generation
        test_bulk_order_generation()
        
        print("\n✅ All tests passed!")
        print("\n📋 Next steps:")
        print("1. Start the main application: npm run dev")
        print("2. Go to http://localhost:3001")
        print("3. Click '📊 Monitoring' button")
        print("4. Try these chat commands:")
        print("   - 'Generate 5 urgent orders'")
        print("   - 'Create a new product called Smart Sensor'")
        print("   - 'Create an order for microprocessors'")
        print("   - 'Show me all orders'")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_agent_integration()
    sys.exit(0 if success else 1)
