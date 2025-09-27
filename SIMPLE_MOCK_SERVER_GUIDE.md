# 🌐 Simple Mock Order Server Guide

This guide explains how to use the simple HTTP-based mock order server for testing the monitoring dashboard.

## 🚀 Quick Start

### 1. Start the Mock Server

```bash
python3 simple_mock_server.py
```

This will start an HTTP server on `http://localhost:8765` that generates realistic mock orders.

### 2. Test the Server

Open your browser and go to:
- **API Documentation**: http://localhost:8765
- **Single Order**: http://localhost:8765/api/orders
- **Batch Orders**: http://localhost:8765/api/orders/batch

### 3. Use in Your Application

The server provides two main endpoints:

#### Single Order Endpoint
```bash
curl http://localhost:8765/api/orders
```

Returns a single random order with realistic data.

#### Batch Orders Endpoint
```bash
curl http://localhost:8765/api/orders/batch
```

Returns 1-3 random orders in a batch.

## 📊 Order Data Structure

Each order includes:

```json
{
  "success": true,
  "data": {
    "id": "ORD-1759008527-5995",
    "supplier": "Budget Suppliers Ltd",
    "products": ["Memory chips", "Steel components"],
    "quantity": 66,
    "total_amount": 2014.46,
    "currency": "USD",
    "status": "processing",
    "priority": "medium",
    "region": "Asia Pacific",
    "order_date": "2025-09-26T15:28:47.782739",
    "expected_delivery": "2025-09-30T14:28:47.782739",
    "tracking_number": "TRK402250",
    "notes": "Regular order processing",
    "created_at": "2025-09-27T14:28:47.782739",
    "pattern_type": "regular_orders"
  },
  "timestamp": "2025-09-27T14:28:47.782739"
}
```

## 🎯 Order Variations

The server generates different types of orders:

| Pattern | Frequency | Priority | Delivery Time | Description |
|---------|-----------|----------|---------------|-------------|
| **Rush Orders** | 10% | Urgent | 1 day | Express delivery required |
| **Bulk Orders** | 15% | Medium | 7 days | Large quantity orders |
| **Regular Orders** | 60% | Medium | 3 days | Standard processing |
| **Premium Orders** | 10% | High | 2 days | VIP customers |
| **Delayed Orders** | 5% | Low | 14 days | Backorder processing |

## 🔧 Integration with Monitoring Dashboard

### Frontend Integration

You can integrate this with your monitoring dashboard by making HTTP requests:

```javascript
// Fetch single order
async function fetchMockOrder() {
  const response = await fetch('http://localhost:8765/api/orders');
  const data = await response.json();
  return data.data;
}

// Fetch batch of orders
async function fetchMockOrders() {
  const response = await fetch('http://localhost:8765/api/orders/batch');
  const data = await response.json();
  return data.data.orders;
}

// Poll for new orders every 5 seconds
setInterval(async () => {
  const orders = await fetchMockOrders();
  updateDashboard(orders);
}, 5000);
```

### React Hook Example

```javascript
import { useState, useEffect } from 'react';

function useMockOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8765/api/orders/batch');
      const data = await response.json();
      if (data.success) {
        setOrders(prev => [...prev, ...data.data.orders]);
      }
    } catch (error) {
      console.error('Failed to fetch orders:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch initial orders
    fetchOrders();
    
    // Poll for new orders every 5 seconds
    const interval = setInterval(fetchOrders, 5000);
    
    return () => clearInterval(interval);
  }, []);

  return { orders, loading, fetchOrders };
}
```

## 🛠️ Customization

### Modify Order Patterns

Edit `simple_mock_server.py` to change order patterns:

```python
self.order_patterns = {
    "rush_orders": {"frequency": 0.2, "priority": "urgent", "delivery_time": 1},
    "bulk_orders": {"frequency": 0.3, "priority": "medium", "delivery_time": 7},
    "regular_orders": {"frequency": 0.4, "priority": "medium", "delivery_time": 3},
    "premium_orders": {"frequency": 0.1, "priority": "high", "delivery_time": 2},
    "delayed_orders": {"frequency": 0.0, "priority": "low", "delivery_time": 14}
}
```

### Add New Suppliers/Products

```python
self.suppliers = [
    "TechCorp Solutions", "Global Parts Inc", "Budget Suppliers Ltd",
    "Premium Components", "FastTrack Logistics", "Reliable Systems",
    "Your New Supplier"  # Add your suppliers here
]

self.products = [
    "Microprocessors", "Memory chips", "Circuit boards", "Steel components",
    "Aluminum parts", "Plastic materials", "Electronic sensors",
    "Power supplies", "Cables", "Connectors",
    "Your New Product"  # Add your products here
]
```

### Change Port

```python
def start_server(port=8765):  # Change port here
    # ... server code
```

## 📈 Monitoring Dashboard Integration

### Real-time Updates

To see variability in your monitoring dashboard:

1. **Start the mock server**:
   ```bash
   python3 simple_mock_server.py
   ```

2. **Start your main application**:
   ```bash
   npm run dev
   ```

3. **Access monitoring dashboard**:
   - Go to `http://localhost:3001`
   - Click "📊 Monitoring" button
   - The dashboard should fetch orders from `http://localhost:8765`

### Dashboard Features to Test

- **Order Status Changes**: Orders moving through different statuses
- **Priority Alerts**: Urgent and high-priority order notifications
- **Regional Distribution**: Orders from different global regions
- **Amount Variations**: Orders with varying monetary values
- **Delivery Time Variability**: Different expected delivery times
- **Supplier Diversity**: Orders from various suppliers

## 🧪 Testing Scenarios

### Scenario 1: High Rush Orders
```python
# Modify patterns to increase rush orders
"rush_orders": {"frequency": 0.5, "priority": "urgent", "delivery_time": 1}
```

### Scenario 2: Bulk Order Processing
```python
# Increase bulk orders
"bulk_orders": {"frequency": 0.4, "priority": "medium", "delivery_time": 7}
```

### Scenario 3: Delayed Order Management
```python
# Increase delayed orders
"delayed_orders": {"frequency": 0.3, "priority": "low", "delivery_time": 14}
```

## 🔍 Debugging

### Check Server Status

```bash
# Check if server is running
curl http://localhost:8765/api/orders

# Check server logs
# Look for output like:
# ✅ Server started on http://localhost:8765
```

### Test Different Endpoints

```bash
# Test single order
curl http://localhost:8765/api/orders | jq '.data.id'

# Test batch orders
curl http://localhost:8765/api/orders/batch | jq '.data.batch_size'

# Test API documentation
curl http://localhost:8765
```

### Common Issues

1. **Port already in use**: Change port in `start_server(port=8766)`
2. **CORS issues**: The server includes CORS headers, but check browser console
3. **No orders appearing**: Check if server is running and accessible

## 📚 Next Steps

1. **Customize order patterns** for your specific use case
2. **Add more realistic data** (prices, suppliers, regions)
3. **Integrate with your monitoring dashboard**
4. **Add order lifecycle management** (status transitions)
5. **Implement order analytics** and reporting

## 🆘 Support

If you encounter issues:

1. **Check server logs** for error messages
2. **Verify server is running** with `curl http://localhost:8765/api/orders`
3. **Check port availability** and firewall settings
4. **Restart the server** if needed

The simple mock server is designed to be lightweight and easy to use for testing your monitoring dashboard! 🎯
