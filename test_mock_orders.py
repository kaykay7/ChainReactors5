#!/usr/bin/env python3
"""
🧪 TEST MOCK ORDER STREAMING
Test script to verify mock order generation works correctly.
"""

import asyncio
import sys
import os
import json

# Add the agent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))

from agent.mock_order_streamer import MockOrderStreamer

async def test_mock_order_generation():
    """Test mock order generation."""
    print("🧪 Testing mock order generation...")
    
    streamer = MockOrderStreamer()
    
    # Generate a few test orders
    for i in range(5):
        order = await streamer.generate_mock_order()
        print(f"\n📦 Order {i+1}:")
        print(f"   ID: {order['id']}")
        print(f"   Supplier: {order['supplier']}")
        print(f"   Products: {', '.join(order['products'])}")
        print(f"   Amount: ${order['total_amount']}")
        print(f"   Status: {order['status']}")
        print(f"   Priority: {order['priority']}")
        print(f"   Pattern: {order['pattern_type']}")
        print(f"   Notes: {order['notes']}")
    
    print("\n✅ Mock order generation test completed!")

async def test_order_patterns():
    """Test different order patterns."""
    print("\n🎯 Testing order patterns...")
    
    streamer = MockOrderStreamer()
    
    # Test each pattern
    for pattern_name, pattern_data in streamer.order_patterns.items():
        print(f"\n📊 Pattern: {pattern_name}")
        print(f"   Frequency: {pattern_data['frequency']*100}%")
        print(f"   Priority: {pattern_data['priority']}")
        print(f"   Delivery Time: {pattern_data['delivery_time']} days")
        
        # Generate a few orders of this pattern
        for i in range(3):
            pattern = {
                "type": pattern_name,
                "priority": pattern_data["priority"],
                "delivery_time": pattern_data["delivery_time"]
            }
            order = await streamer.generate_mock_order()
            print(f"   Order {i+1}: {order['id']} - ${order['total_amount']} - {order['notes']}")

async def main():
    """Run all tests."""
    print("🚀 Starting mock order streaming tests...")
    print("=" * 50)
    
    try:
        await test_mock_order_generation()
        await test_order_patterns()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run: python start_mock_streaming.py")
        print("2. Open monitoring dashboard")
        print("3. Watch real-time order data!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
