# 🏪 Amazon-Style Supply Chain Dashboard

## 🎯 **Overview: Amazon-Style Real-Time Management**

This implementation creates an Amazon-style supply chain management dashboard with real-time updates for low stock alerts, shipping delays, supplier issues, and other critical supply chain events.

## 🏗️ **Dashboard Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                    AMAZON-STYLE DASHBOARD                       │
├─────────────────────────────────────────────────────────────────┤
│  🏪 Real-Time Monitoring    📊 Dashboard Metrics                │
│  ├── Low Stock Alerts      ├── Total Items                    │
│  ├── Shipping Delays       ├── On-Time Delivery               │
│  ├── Supplier Issues       ├── Supplier Performance           │
│  ├── Demand Surges         ├── Inventory Value                │
│  ├── Price Changes         └── Cost Savings                    │
│  └── Quality Issues                                            │
└─────────────────────────────────────────────────────────────────┘
                                ↕️
┌─────────────────────────────────────────────────────────────────┐
│                    REAL-TIME ALERTS                            │
├─────────────────────────────────────────────────────────────────┤
│  🔔 Alert System          📡 WebSocket Streaming               │
│  ├── Critical Alerts      ├── Live Updates                     │
│  ├── High Priority        ├── Event Broadcasting              │
│  ├── Medium Priority      ├── Multi-Client Support             │
│  ├── Low Priority         └── Auto-Reconnect                    │
│  └── Alert History                                            │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 **Quick Start**

### **1. Start the Amazon Dashboard Server**
```bash
python3 start_amazon_dashboard.py
```

### **2. Use the Amazon Dashboard Component**
```typescript
// In src/app/page.tsx
import AmazonDashboard from "@/components/AmazonDashboard";

export default function CopilotKitPage() {
  return <AmazonDashboard />;
}
```

### **3. Access the Dashboard**
- **WebSocket**: `ws://localhost:8765`
- **HTTP API**: `http://localhost:9001`
- **Dashboard**: Your Next.js app with real-time updates

## 🎯 **Key Features**

### **✅ Real-Time Alerts**
- **Low Stock Alerts** - Items running low on inventory
- **Shipping Delays** - Delivery delays and tracking issues
- **Supplier Issues** - Performance problems and quality issues
- **Demand Surges** - Unexpected demand increases
- **Price Changes** - Cost fluctuations and market changes
- **Quality Issues** - Product quality problems

### **✅ Dashboard Metrics**
- **Total Items** - Complete inventory count
- **Low Stock Items** - Items needing reorder
- **On-Time Delivery** - Delivery performance percentage
- **Supplier Performance** - Supplier reliability scores
- **Inventory Value** - Total inventory worth
- **Cost Savings** - Efficiency improvements

### **✅ Alert Management**
- **Acknowledge Alerts** - Mark alerts as reviewed
- **Resolve Alerts** - Close resolved issues
- **Priority Scoring** - Intelligent alert prioritization
- **Alert History** - Track all past alerts
- **Real-Time Updates** - Live alert notifications

## 🛠️ **Implementation Details**

### **1. Backend Monitoring System**

#### **AmazonStyleMonitor**
```python
class AmazonStyleMonitor:
    async def start_monitoring(self):
        # Start real-time monitoring tasks
        asyncio.create_task(self._monitor_inventory_levels())
        asyncio.create_task(self._monitor_shipping_status())
        asyncio.create_task(self._monitor_supplier_performance())
        asyncio.create_task(self._monitor_demand_patterns())
        asyncio.create_task(self._monitor_price_changes())
```

#### **Alert Types**
```python
class AlertType(Enum):
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    SHIPPING_DELAY = "shipping_delay"
    SUPPLIER_ISSUE = "supplier_issue"
    QUALITY_ISSUE = "quality_issue"
    DEMAND_SURGE = "demand_surge"
    PRICE_CHANGE = "price_change"
    DELIVERY_DELAY = "delivery_delay"
    INVENTORY_ANOMALY = "inventory_anomaly"
    SUPPLIER_PERFORMANCE = "supplier_performance"
```

#### **Alert Severity**
```python
class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
```

### **2. Frontend Dashboard**

#### **AmazonDashboard Component**
```typescript
// Real-time dashboard with Amazon-style interface
export default function AmazonDashboard() {
  const { isConnected, events, responses, sendUserRequest } = useStreaming();
  const [metrics, setMetrics] = useState<DashboardMetrics>({...});
  const [alerts, setAlerts] = useState<SupplyChainAlert[]>([]);
  
  // Handle real-time updates
  useEffect(() => {
    events.forEach(event => {
      if (event.event_type === 'supply_chain_alert') {
        setAlerts(prev => [event.data, ...prev]);
      }
    });
  }, [events]);
}
```

#### **useAmazonDashboard Hook**
```typescript
// Specialized hook for Amazon-style dashboard
const {
  isConnected,
  dashboardData,
  alerts,
  metrics,
  acknowledgeAlert,
  resolveAlert
} = useAmazonDashboard();
```

## 🎯 **Dashboard Components**

### **1. 📊 Key Metrics Cards**
- **Total Items** - Complete inventory count
- **Low Stock** - Items needing attention
- **On-Time Delivery** - Performance percentage
- **Inventory Value** - Total worth

### **2. 🔔 Active Alerts Panel**
- **Real-time alerts** with severity indicators
- **Alert details** with recommended actions
- **Acknowledge/Resolve** buttons
- **Priority scoring** system

### **3. 📈 Performance Metrics**
- **Supplier Performance** - Reliability scores
- **On-Time Deliveries** - Delivery metrics
- **Cost Savings** - Efficiency gains
- **Critical Alerts** - High-priority issues

### **4. 🤖 AI Assistant**
- **Natural language** alert management
- **Intelligent insights** and recommendations
- **Automated responses** to common issues
- **Predictive analytics** for future problems

## 🎯 **Usage Examples**

### **1. 🔔 Real-Time Alert Management**
```
User: "Show me all critical alerts"
AI: Displays critical alerts with details and actions
```

### **2. 📊 Performance Monitoring**
```
User: "How are our suppliers performing?"
AI: Shows supplier performance metrics and alerts
```

### **3. 🚚 Shipping Status**
```
User: "Any shipping delays today?"
AI: Lists all shipping delay alerts with tracking info
```

### **4. 📦 Inventory Management**
```
User: "What items are low on stock?"
AI: Shows low stock alerts with reorder recommendations
```

## 🔧 **Configuration**

### **Alert Thresholds**
```python
# Customize alert generation probabilities
LOW_STOCK_PROBABILITY = 0.3  # 30% chance every 5 seconds
SHIPPING_DELAY_PROBABILITY = 0.2  # 20% chance every 10 seconds
SUPPLIER_ISSUE_PROBABILITY = 0.15  # 15% chance every 15 seconds
DEMAND_SURGE_PROBABILITY = 0.1  # 10% chance every 20 seconds
PRICE_CHANGE_PROBABILITY = 0.05  # 5% chance every 30 seconds
```

### **WebSocket Configuration**
```typescript
// Default: ws://localhost:8765
const { isConnected, alerts, metrics } = useAmazonDashboard('ws://your-server:8765');
```

### **Server Configuration**
```python
# Default: 9001
uvicorn.run(app, host="0.0.0.0", port=9001)
```

## 🎉 **Benefits**

### **✅ Amazon-Style Experience**
- **Real-time monitoring** like Amazon's dashboard
- **Proactive alerts** for supply chain issues
- **Intelligent prioritization** of critical events
- **Comprehensive metrics** and performance tracking

### **✅ Supply Chain Optimization**
- **Early warning system** for potential issues
- **Automated recommendations** for problem resolution
- **Performance tracking** across all suppliers
- **Cost optimization** through better visibility

### **✅ Enhanced Decision Making**
- **Real-time data** for informed decisions
- **Historical tracking** of alert patterns
- **Predictive insights** for future planning
- **Collaborative resolution** with AI assistance

### **✅ Scalable Architecture**
- **Multi-client support** for team collaboration
- **Event-driven updates** for efficient processing
- **WebSocket streaming** for real-time communication
- **Modular design** for easy extension

## 🚀 **Advanced Features**

### **Custom Alert Rules**
```python
# Define custom alert conditions
if inventory_level < reorder_point:
    generate_low_stock_alert()
if delivery_delay > threshold:
    generate_shipping_delay_alert()
```

### **Alert Escalation**
```python
# Automatic escalation for critical alerts
if alert.severity == AlertSeverity.CRITICAL:
    escalate_to_management()
    notify_stakeholders()
```

### **Performance Analytics**
```python
# Track alert resolution times
resolution_time = alert.resolved_at - alert.created_at
update_performance_metrics(resolution_time)
```

## 🔍 **Troubleshooting**

### **Connection Issues**
```typescript
// Check connection status
console.log('Connected:', isConnected);

// Manual reconnect
const { connect, disconnect } = useAmazonDashboard();
disconnect();
connect();
```

### **Alert Management**
```typescript
// Acknowledge alert
acknowledgeAlert('alert_123');

// Resolve alert
resolveAlert('alert_123');
```

### **Server Issues**
```bash
# Check server logs
python3 start_amazon_dashboard.py

# Test WebSocket connection
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Sec-WebSocket-Key: test" -H "Sec-WebSocket-Version: 13" http://localhost:8765
```

## 🎯 **Summary**

This Amazon-style dashboard provides:

1. **🏪 Real-Time Monitoring** - Live supply chain event tracking
2. **🔔 Intelligent Alerts** - Proactive issue detection and notification
3. **📊 Performance Metrics** - Comprehensive KPI tracking
4. **🤖 AI Integration** - Smart recommendations and automation
5. **📱 Responsive Design** - Works on all devices
6. **🔄 Live Updates** - Real-time data synchronization
7. **⚡ Fast Response** - Immediate alert handling and resolution

**Result**: A powerful, Amazon-style supply chain management system with real-time monitoring, intelligent alerts, and comprehensive analytics! 🚀
