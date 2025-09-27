"""
🏪 AMAZON-STYLE SUPPLY CHAIN MONITOR
Real-time monitoring system for supply chain events like Amazon's dashboard.
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, AsyncGenerator
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import random

class AlertType(Enum):
    """Types of supply chain alerts."""
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

class AlertSeverity(Enum):
    """Alert severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SupplyChainAlert:
    """Supply chain alert structure."""
    alert_id: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    description: str
    affected_items: List[str]
    affected_suppliers: List[str]
    timestamp: datetime
    estimated_impact: str
    recommended_actions: List[str]
    status: str = "active"  # active, acknowledged, resolved
    priority_score: int = 0

@dataclass
class DashboardMetrics:
    """Dashboard metrics structure."""
    total_items: int
    low_stock_items: int
    out_of_stock_items: int
    active_alerts: int
    critical_alerts: int
    on_time_deliveries: float
    supplier_performance: float
    inventory_value: float
    cost_savings: float

class AmazonStyleMonitor:
    """Amazon-style supply chain monitoring system."""
    
    def __init__(self):
        self.active_alerts: List[SupplyChainAlert] = []
        self.metrics: DashboardMetrics = DashboardMetrics(0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0)
        self.monitoring_active = False
        self.alert_history: List[SupplyChainAlert] = []
        self.subscribers: List[Any] = []  # WebSocket connections
        
    async def start_monitoring(self):
        """Start the real-time monitoring system."""
        self.monitoring_active = True
        print("🏪 Amazon-style monitoring started")
        
        # Start monitoring tasks
        asyncio.create_task(self._monitor_inventory_levels())
        asyncio.create_task(self._monitor_shipping_status())
        asyncio.create_task(self._monitor_supplier_performance())
        asyncio.create_task(self._monitor_demand_patterns())
        asyncio.create_task(self._monitor_price_changes())
        
    async def stop_monitoring(self):
        """Stop the monitoring system."""
        self.monitoring_active = False
        print("🏪 Monitoring stopped")
    
    async def add_subscriber(self, websocket):
        """Add a subscriber for real-time updates."""
        self.subscribers.append(websocket)
        print(f"📡 Subscriber added. Total: {len(self.subscribers)}")
    
    async def remove_subscriber(self, websocket):
        """Remove a subscriber."""
        if websocket in self.subscribers:
            self.subscribers.remove(websocket)
        print(f"📡 Subscriber removed. Total: {len(self.subscribers)}")
    
    async def broadcast_alert(self, alert: SupplyChainAlert):
        """Broadcast alert to all subscribers."""
        if not self.subscribers:
            return
        
        alert_data = {
            "type": "supply_chain_alert",
            "alert": {
                "alert_id": alert.alert_id,
                "alert_type": alert.alert_type.value,
                "severity": alert.severity.value,
                "title": alert.title,
                "description": alert.description,
                "affected_items": alert.affected_items,
                "affected_suppliers": alert.affected_suppliers,
                "timestamp": alert.timestamp.isoformat(),
                "estimated_impact": alert.estimated_impact,
                "recommended_actions": alert.recommended_actions,
                "status": alert.status,
                "priority_score": alert.priority_score
            }
        }
        
        # Send to all subscribers
        disconnected = []
        for subscriber in self.subscribers:
            try:
                await subscriber.send(json.dumps(alert_data))
            except Exception:
                disconnected.append(subscriber)
        
        # Remove disconnected subscribers
        for sub in disconnected:
            await self.remove_subscriber(sub)
    
    async def broadcast_metrics(self, metrics: DashboardMetrics):
        """Broadcast dashboard metrics to all subscribers."""
        if not self.subscribers:
            return
        
        metrics_data = {
            "type": "dashboard_metrics",
            "metrics": {
                "total_items": metrics.total_items,
                "low_stock_items": metrics.low_stock_items,
                "out_of_stock_items": metrics.out_of_stock_items,
                "active_alerts": metrics.active_alerts,
                "critical_alerts": metrics.critical_alerts,
                "on_time_deliveries": metrics.on_time_deliveries,
                "supplier_performance": metrics.supplier_performance,
                "inventory_value": metrics.inventory_value,
                "cost_savings": metrics.cost_savings,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Send to all subscribers
        disconnected = []
        for subscriber in self.subscribers:
            try:
                await subscriber.send(json.dumps(metrics_data))
            except Exception:
                disconnected.append(subscriber)
        
        # Remove disconnected subscribers
        for sub in disconnected:
            await self.remove_subscriber(sub)
    
    async def _monitor_inventory_levels(self):
        """Monitor inventory levels for low stock alerts."""
        while self.monitoring_active:
            try:
                # Simulate inventory monitoring
                await asyncio.sleep(5)  # Check every 5 seconds
                
                # Generate random low stock alerts
                if random.random() < 0.3:  # 30% chance of alert
                    alert = await self._generate_low_stock_alert()
                    if alert:
                        self.active_alerts.append(alert)
                        self.alert_history.append(alert)
                        await self.broadcast_alert(alert)
                        await self._update_metrics()
                
            except Exception as e:
                print(f"❌ Error monitoring inventory: {e}")
    
    async def _monitor_shipping_status(self):
        """Monitor shipping status for delays."""
        while self.monitoring_active:
            try:
                await asyncio.sleep(10)  # Check every 10 seconds
                
                # Generate random shipping delay alerts
                if random.random() < 0.2:  # 20% chance of delay
                    alert = await self._generate_shipping_delay_alert()
                    if alert:
                        self.active_alerts.append(alert)
                        self.alert_history.append(alert)
                        await self.broadcast_alert(alert)
                        await self._update_metrics()
                
            except Exception as e:
                print(f"❌ Error monitoring shipping: {e}")
    
    async def _monitor_supplier_performance(self):
        """Monitor supplier performance."""
        while self.monitoring_active:
            try:
                await asyncio.sleep(15)  # Check every 15 seconds
                
                # Generate random supplier performance alerts
                if random.random() < 0.15:  # 15% chance of issue
                    alert = await self._generate_supplier_alert()
                    if alert:
                        self.active_alerts.append(alert)
                        self.alert_history.append(alert)
                        await self.broadcast_alert(alert)
                        await self._update_metrics()
                
            except Exception as e:
                print(f"❌ Error monitoring suppliers: {e}")
    
    async def _monitor_demand_patterns(self):
        """Monitor demand patterns for surges."""
        while self.monitoring_active:
            try:
                await asyncio.sleep(20)  # Check every 20 seconds
                
                # Generate random demand surge alerts
                if random.random() < 0.1:  # 10% chance of surge
                    alert = await self._generate_demand_surge_alert()
                    if alert:
                        self.active_alerts.append(alert)
                        self.alert_history.append(alert)
                        await self.broadcast_alert(alert)
                        await self._update_metrics()
                
            except Exception as e:
                print(f"❌ Error monitoring demand: {e}")
    
    async def _monitor_price_changes(self):
        """Monitor price changes."""
        while self.monitoring_active:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds
                
                # Generate random price change alerts
                if random.random() < 0.05:  # 5% chance of price change
                    alert = await self._generate_price_change_alert()
                    if alert:
                        self.active_alerts.append(alert)
                        self.alert_history.append(alert)
                        await self.broadcast_alert(alert)
                        await self._update_metrics()
                
            except Exception as e:
                print(f"❌ Error monitoring prices: {e}")
    
    async def _generate_low_stock_alert(self) -> Optional[SupplyChainAlert]:
        """Generate a low stock alert."""
        products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
        suppliers = ["TechCorp Solutions", "Global Parts Inc", "Budget Suppliers Ltd"]
        
        product = random.choice(products)
        supplier = random.choice(suppliers)
        
        return SupplyChainAlert(
            alert_id=f"low_stock_{datetime.now().timestamp()}",
            alert_type=AlertType.LOW_STOCK,
            severity=AlertSeverity.MEDIUM,
            title=f"Low Stock Alert: {product}",
            description=f"{product} is running low on stock. Current level: {random.randint(5, 15)} units",
            affected_items=[product],
            affected_suppliers=[supplier],
            timestamp=datetime.now(),
            estimated_impact=f"Potential stockout in {random.randint(2, 7)} days",
            recommended_actions=[
                f"Reorder {product} from {supplier}",
                "Consider alternative suppliers",
                "Review demand forecasting"
            ],
            priority_score=random.randint(60, 80)
        )
    
    async def _generate_shipping_delay_alert(self) -> Optional[SupplyChainAlert]:
        """Generate a shipping delay alert."""
        shipments = ["SHIP-001", "SHIP-002", "SHIP-003", "SHIP-004"]
        carriers = ["FedEx", "UPS", "DHL", "USPS"]
        
        shipment = random.choice(shipments)
        carrier = random.choice(carriers)
        delay_days = random.randint(1, 5)
        
        return SupplyChainAlert(
            alert_id=f"shipping_delay_{datetime.now().timestamp()}",
            alert_type=AlertType.SHIPPING_DELAY,
            severity=AlertSeverity.HIGH,
            title=f"Shipping Delay: {shipment}",
            description=f"Shipment {shipment} via {carrier} is delayed by {delay_days} days",
            affected_items=[shipment],
            affected_suppliers=[carrier],
            timestamp=datetime.now(),
            estimated_impact=f"Delivery delayed by {delay_days} days",
            recommended_actions=[
                f"Contact {carrier} for updated tracking",
                "Notify customers of delay",
                "Consider expedited shipping for critical items"
            ],
            priority_score=random.randint(70, 90)
        )
    
    async def _generate_supplier_alert(self) -> Optional[SupplyChainAlert]:
        """Generate a supplier performance alert."""
        suppliers = ["TechCorp Solutions", "Global Parts Inc", "Budget Suppliers Ltd"]
        issues = ["Quality issues", "Delivery delays", "Communication problems", "Price increases"]
        
        supplier = random.choice(suppliers)
        issue = random.choice(issues)
        
        return SupplyChainAlert(
            alert_id=f"supplier_{datetime.now().timestamp()}",
            alert_type=AlertType.SUPPLIER_ISSUE,
            severity=AlertSeverity.MEDIUM,
            title=f"Supplier Issue: {supplier}",
            description=f"{supplier} is experiencing {issue.lower()}",
            affected_items=[],
            affected_suppliers=[supplier],
            timestamp=datetime.now(),
            estimated_impact="Potential supply chain disruption",
            recommended_actions=[
                f"Contact {supplier} for resolution",
                "Activate backup suppliers",
                "Review supplier performance metrics"
            ],
            priority_score=random.randint(50, 75)
        )
    
    async def _generate_demand_surge_alert(self) -> Optional[SupplyChainAlert]:
        """Generate a demand surge alert."""
        products = ["Product A", "Product B", "Product C"]
        surge_percentage = random.randint(150, 300)
        
        product = random.choice(products)
        
        return SupplyChainAlert(
            alert_id=f"demand_surge_{datetime.now().timestamp()}",
            alert_type=AlertType.DEMAND_SURGE,
            severity=AlertSeverity.HIGH,
            title=f"Demand Surge: {product}",
            description=f"{product} demand increased by {surge_percentage}%",
            affected_items=[product],
            affected_suppliers=[],
            timestamp=datetime.now(),
            estimated_impact="Potential stockout risk",
            recommended_actions=[
                f"Increase {product} inventory levels",
                "Contact suppliers for additional capacity",
                "Review pricing strategy"
            ],
            priority_score=random.randint(80, 95)
        )
    
    async def _generate_price_change_alert(self) -> Optional[SupplyChainAlert]:
        """Generate a price change alert."""
        products = ["Product A", "Product B", "Product C"]
        price_change = random.randint(-20, 20)
        
        product = random.choice(products)
        change_type = "increased" if price_change > 0 else "decreased"
        
        return SupplyChainAlert(
            alert_id=f"price_change_{datetime.now().timestamp()}",
            alert_type=AlertType.PRICE_CHANGE,
            severity=AlertSeverity.LOW,
            title=f"Price Change: {product}",
            description=f"{product} price {change_type} by {abs(price_change)}%",
            affected_items=[product],
            affected_suppliers=[],
            timestamp=datetime.now(),
            estimated_impact=f"Cost impact: {abs(price_change)}%",
            recommended_actions=[
                "Review pricing strategy",
                "Update cost calculations",
                "Communicate changes to stakeholders"
            ],
            priority_score=random.randint(30, 60)
        )
    
    async def _update_metrics(self):
        """Update dashboard metrics."""
        self.metrics = DashboardMetrics(
            total_items=random.randint(100, 500),
            low_stock_items=len([a for a in self.active_alerts if a.alert_type == AlertType.LOW_STOCK]),
            out_of_stock_items=len([a for a in self.active_alerts if a.alert_type == AlertType.OUT_OF_STOCK]),
            active_alerts=len(self.active_alerts),
            critical_alerts=len([a for a in self.active_alerts if a.severity == AlertSeverity.CRITICAL]),
            on_time_deliveries=random.uniform(85, 98),
            supplier_performance=random.uniform(75, 95),
            inventory_value=random.uniform(100000, 500000),
            cost_savings=random.uniform(5000, 25000)
        )
        
        await self.broadcast_metrics(self.metrics)
    
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """Get current dashboard data."""
        return {
            "metrics": {
                "total_items": self.metrics.total_items,
                "low_stock_items": self.metrics.low_stock_items,
                "out_of_stock_items": self.metrics.out_of_stock_items,
                "active_alerts": self.metrics.active_alerts,
                "critical_alerts": self.metrics.critical_alerts,
                "on_time_deliveries": self.metrics.on_time_deliveries,
                "supplier_performance": self.metrics.supplier_performance,
                "inventory_value": self.metrics.inventory_value,
                "cost_savings": self.metrics.cost_savings
            },
            "active_alerts": [
                {
                    "alert_id": alert.alert_id,
                    "alert_type": alert.alert_type.value,
                    "severity": alert.severity.value,
                    "title": alert.title,
                    "description": alert.description,
                    "affected_items": alert.affected_items,
                    "affected_suppliers": alert.affected_suppliers,
                    "timestamp": alert.timestamp.isoformat(),
                    "estimated_impact": alert.estimated_impact,
                    "recommended_actions": alert.recommended_actions,
                    "status": alert.status,
                    "priority_score": alert.priority_score
                }
                for alert in self.active_alerts
            ],
            "alert_history": [
                {
                    "alert_id": alert.alert_id,
                    "alert_type": alert.alert_type.value,
                    "severity": alert.severity.value,
                    "title": alert.title,
                    "timestamp": alert.timestamp.isoformat(),
                    "status": alert.status
                }
                for alert in self.alert_history[-50:]  # Last 50 alerts
            ]
        }
    
    async def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert."""
        for alert in self.active_alerts:
            if alert.alert_id == alert_id:
                alert.status = "acknowledged"
                await self.broadcast_alert(alert)
                return True
        return False
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert."""
        for alert in self.active_alerts:
            if alert.alert_id == alert_id:
                alert.status = "resolved"
                self.active_alerts.remove(alert)
                await self.broadcast_alert(alert)
                await self._update_metrics()
                return True
        return False
