# 📦 Mock Order Streaming Guide

This guide explains how to set up and use mock order streaming to see variability in the monitoring dashboard.

## 🎯 Overview

The mock order streamer generates realistic order data with variations to test the monitoring dashboard. It creates different types of orders with varying priorities, delivery times, and statuses.

## 🚀 Quick Start

### 1. Start the Mock Order Streaming Server

```bash
# Start the WebSocket server with mock order streaming
python start_mock_streaming.py
```

This will:
- Start a WebSocket server on `ws://localhost:8765`
- Begin generating mock orders with realistic variations
- Stream orders to connected clients every 2-8 seconds

### 2. Access the Monitoring Dashboard

1. **Start the main application**:
   ```bash
   npm run dev
   ```

2. **Navigate to monitoring**:
   - Go to `http://localhost:3001`
   - Click the "📊 Monitoring" button in the header
   - Or go directly to `http://localhost:3001/monitoring`

3. **View real-time order data**:
   - The dashboard will show incoming orders
   - Orders will appear with different statuses and priorities
   - You'll see variability in delivery times and amounts

## 📊 Order Variations

The mock streamer generates several types of orders:

### Order Patterns

| Pattern | Frequency | Priority | Delivery Time | Description |
|---------|-----------|----------|---------------|-------------|
| **Rush Orders** | 10% | Urgent | 1 day | Express delivery required |
| **Bulk Orders** | 15% | Medium | 7 days | Large quantity orders |
| **Regular Orders** | 60% | Medium | 3 days | Standard processing |
| **Premium Orders** | 10% | High | 2 days | VIP customers |
| **Delayed Orders** | 5% | Low | 14 days | Backorder processing |

### Order Data Fields

Each mock order includes:

```json
{
  "id": "ORD-1703123456-7890",
  "supplier": "TechCorp Solutions",
  "products": ["Microprocessors", "Memory chips"],
  "quantity": 50,
  "total_amount": 1250.75,
  "currency": "USD",
  "status": "confirmed",
  "priority": "urgent",
  "region": "North America",
  "order_date": "2024-01-15T10:30:00",
  "expected_delivery": "2024-01-16T18:00:00",
  "tracking_number": "TRK123456",
  "notes": "Express delivery required",
  "created_at": "2024-01-15T10:30:00",
  "pattern_type": "rush_orders"
}
```

## 🔧 Configuration

### Customizing Order Patterns

Edit `agent/agent/mock_order_streamer.py` to modify:

```python
# Order patterns for realistic variations
self.order_patterns = {
    "rush_orders": {"frequency": 0.1, "priority": "urgent", "delivery_time": 1},
    "bulk_orders": {"frequency": 0.15, "priority": "medium", "delivery_time": 7},
    "regular_orders": {"frequency": 0.6, "priority": "medium", "delivery_time": 3},
    "premium_orders": {"frequency": 0.1, "priority": "high", "delivery_time": 2},
    "delayed_orders": {"frequency": 0.05, "priority": "low", "delivery_time": 14}
}
```

### Adjusting Streaming Frequency

```python
# Wait between batches (2-8 seconds)
await asyncio.sleep(random.uniform(2, 8))
```

### Adding New Suppliers/Products

```python
self.suppliers = [
    "TechCorp Solutions", "Global Parts Inc", "Budget Suppliers Ltd",
    "Premium Components", "FastTrack Logistics", "Reliable Systems"
]

self.products = [
    "Microprocessors", "Memory chips", "Circuit boards", "Steel components",
    "Aluminum parts", "Plastic materials", "Electronic sensors",
    "Power supplies", "Cables", "Connectors"
]
```

## 📈 Monitoring Dashboard Features

The monitoring dashboard will show:

### Real-time Metrics
- **Total Orders**: Count of all orders
- **Pending Orders**: Orders awaiting processing
- **Shipped Orders**: Orders in transit
- **Delayed Orders**: Orders past expected delivery

### Order Status Distribution
- Pie chart showing order statuses
- Real-time updates as orders change status

### Priority Alerts
- **Urgent Orders**: Red alerts for rush orders
- **High Priority**: Orange alerts for premium orders
- **Delayed Orders**: Yellow alerts for overdue orders

### Regional Distribution
- Orders by region (North America, Europe, Asia Pacific, etc.)
- Geographic insights for supply chain optimization

## 🛠️ Troubleshooting

### WebSocket Connection Issues

1. **Check if server is running**:
   ```bash
   # Look for this output:
   🌐 WebSocket server started on ws://localhost:8765
   📦 Mock order streaming started
   ```

2. **Verify port availability**:
   ```bash
   lsof -i :8765
   ```

3. **Check firewall settings** if using remote connections

### No Orders Appearing

1. **Verify WebSocket connection** in browser dev tools
2. **Check console for errors** in the monitoring dashboard
3. **Restart the streaming server** if needed

### Performance Issues

1. **Reduce batch size** in `generate_mock_order()`
2. **Increase sleep time** between batches
3. **Limit number of connected clients**

## 🎮 Testing Scenarios

### Scenario 1: Rush Order Simulation
- Increase `rush_orders` frequency to 0.3
- Watch for urgent alerts in dashboard
- Verify express delivery processing

### Scenario 2: Bulk Order Processing
- Increase `bulk_orders` frequency to 0.4
- Monitor inventory levels
- Check warehouse capacity alerts

### Scenario 3: Delayed Order Management
- Increase `delayed_orders` frequency to 0.2
- Watch for delay alerts
- Test customer notification systems

## 📝 Logs and Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Monitor Order Generation

```python
# Add to mock_order_streamer.py
print(f"📦 Generated {len(orders)} orders: {[o['id'] for o in orders]}")
```

### WebSocket Message Logging

```python
# Add to websocket_server.py
print(f"📨 Received: {message}")
print(f"📤 Sent: {json.dumps(message)}")
```

## 🚀 Advanced Usage

### Custom Order Generators

Create specialized order generators:

```python
class CustomOrderGenerator:
    def generate_electronics_orders(self):
        # Generate electronics-specific orders
        pass
    
    def generate_automotive_orders(self):
        # Generate automotive-specific orders
        pass
```

### Integration with Real Data

```python
# Mix real and mock data
real_orders = await fetch_real_orders()
mock_orders = await generate_mock_orders()
combined_orders = real_orders + mock_orders
```

### Performance Monitoring

```python
# Track order generation performance
start_time = time.time()
orders = await generate_mock_order()
generation_time = time.time() - start_time
print(f"Order generation took {generation_time:.3f}s")
```

## 📚 Next Steps

1. **Customize order patterns** for your specific use case
2. **Add more realistic data** (prices, suppliers, regions)
3. **Integrate with real APIs** for hybrid data
4. **Add order lifecycle management** (status transitions)
5. **Implement order analytics** and reporting

## 🆘 Support

If you encounter issues:

1. **Check the logs** for error messages
2. **Verify WebSocket connection** in browser dev tools
3. **Restart the streaming server** if needed
4. **Check port availability** and firewall settings

The mock order streaming system is designed to be flexible and easy to customize for your specific testing needs! 🎯
