"""
Supply Chain Optimization Agent Implementation

This module provides advanced supply chain optimization capabilities including:
- Inventory management and demand forecasting
- Supplier performance assessment
- Risk analysis and mitigation
- Cost optimization
- Compliance monitoring
- Logistics optimization
"""

from typing import Dict, List, Any, Optional, Tuple
import json
import math
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    DELAYED = "delayed"

class InventoryStatus(Enum):
    IN_STOCK = "in stock"
    LOW_STOCK = "low stock"
    OUT_OF_STOCK = "out of stock"
    OVERSTOCK = "overstock"

@dataclass
class SupplierMetrics:
    """Supplier performance metrics"""
    reliability_score: float  # 0-100
    average_delivery_time: float  # days
    on_time_delivery_rate: float  # percentage
    quality_score: float  # 0-100
    cost_competitiveness: float  # 0-100
    communication_score: float  # 0-100
    risk_level: RiskLevel

@dataclass
class InventoryItem:
    """Inventory item with optimization data"""
    sku: str
    name: str
    current_stock: int
    min_stock: int
    max_stock: int
    reorder_point: int
    lead_time: int  # days
    unit_cost: float
    demand_rate: float  # units per day
    safety_stock: int
    supplier: str
    status: InventoryStatus

@dataclass
class OrderOptimization:
    """Order optimization recommendations"""
    recommended_quantity: int
    total_cost: float
    delivery_date: str
    supplier: str
    risk_assessment: RiskLevel
    cost_savings: float
    alternative_suppliers: List[str]

class SupplyChainOptimizer:
    """Main supply chain optimization engine"""
    
    def __init__(self):
        self.suppliers: Dict[str, SupplierMetrics] = {}
        self.inventory: Dict[str, InventoryItem] = {}
        self.orders: List[Dict[str, Any]] = []
        self.risk_factors: Dict[str, float] = {}
    
    def analyze_inventory_levels(self, canvas_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current inventory levels and identify optimization opportunities"""
        inventory_items = [item for item in canvas_state.get("items", []) if item.get("type") == "inventory"]
        
        analysis = {
            "total_items": len(inventory_items),
            "low_stock_items": [],
            "overstock_items": [],
            "out_of_stock_items": [],
            "reorder_recommendations": [],
            "cost_analysis": {},
            "risk_assessment": {}
        }
        
        total_inventory_value = 0
        critical_items = 0
        
        for item in inventory_items:
            data = item.get("data", {})
            current_stock = data.get("field3", 0)
            min_stock = data.get("field4", 0)
            max_stock = data.get("field5", 0)
            unit_cost = data.get("field8", 0)
            status = data.get("field12", "in stock")
            
            item_value = current_stock * unit_cost
            total_inventory_value += item_value
            
            # Identify low stock items
            if current_stock <= min_stock:
                analysis["low_stock_items"].append({
                    "item": item.get("name", ""),
                    "sku": data.get("field2", ""),
                    "current_stock": current_stock,
                    "min_stock": min_stock,
                    "status": status
                })
                critical_items += 1
            
            # Identify overstock items
            if current_stock > max_stock * 1.2:  # 20% over max
                analysis["overstock_items"].append({
                    "item": item.get("name", ""),
                    "sku": data.get("field2", ""),
                    "current_stock": current_stock,
                    "max_stock": max_stock,
                    "excess_value": (current_stock - max_stock) * unit_cost
                })
            
            # Identify out of stock items
            if current_stock == 0:
                analysis["out_of_stock_items"].append({
                    "item": item.get("name", ""),
                    "sku": data.get("field2", ""),
                    "supplier": data.get("field9", ""),
                    "lead_time": data.get("field11", 0)
                })
        
        analysis["cost_analysis"] = {
            "total_inventory_value": total_inventory_value,
            "average_item_value": total_inventory_value / len(inventory_items) if inventory_items else 0,
            "critical_items_count": critical_items
        }
        
        analysis["risk_assessment"] = {
            "supply_risk": "high" if critical_items > len(inventory_items) * 0.2 else "medium",
            "inventory_turnover": self._calculate_inventory_turnover(inventory_items),
            "recommendations": self._generate_inventory_recommendations(analysis)
        }
        
        return analysis
    
    def calculate_optimal_reorder_points(self, canvas_state: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate optimal reorder points using demand forecasting"""
        inventory_items = [item for item in canvas_state.get("items", []) if item.get("type") == "inventory"]
        
        recommendations = {
            "reorder_points": [],
            "safety_stock": [],
            "demand_forecasts": [],
            "cost_optimization": {}
        }
        
        for item in inventory_items:
            data = item.get("data", {})
            sku = data.get("field2", "")
            name = item.get("name", "")
            current_stock = data.get("field3", 0)
            lead_time = data.get("field11", 0)
            unit_cost = data.get("field8", 0)
            
            # Calculate demand rate (simplified - in real implementation, use historical data)
            demand_rate = self._estimate_demand_rate(sku, current_stock)
            
            # Calculate safety stock based on lead time and demand variability
            safety_stock = self._calculate_safety_stock(demand_rate, lead_time)
            
            # Calculate optimal reorder point
            reorder_point = int(demand_rate * lead_time + safety_stock)
            
            # Calculate economic order quantity (EOQ)
            eoq = self._calculate_eoq(demand_rate, unit_cost)
            
            recommendations["reorder_points"].append({
                "item": name,
                "sku": sku,
                "current_reorder_point": data.get("field6", 0),
                "recommended_reorder_point": reorder_point,
                "safety_stock": safety_stock,
                "economic_order_quantity": eoq,
                "annual_demand": demand_rate * 365,
                "cost_impact": abs(reorder_point - data.get("field6", 0)) * unit_cost
            })
        
        return recommendations
    
    def assess_supplier_performance(self, canvas_state: Dict[str, Any]) -> Dict[str, Any]:
        """Assess supplier performance and generate recommendations"""
        suppliers = [item for item in canvas_state.get("items", []) if item.get("type") == "supplier"]
        orders = [item for item in canvas_state.get("items", []) if item.get("type") == "order"]
        
        performance_analysis = {
            "supplier_rankings": [],
            "performance_metrics": {},
            "risk_assessments": {},
            "recommendations": []
        }
        
        for supplier in suppliers:
            data = supplier.get("data", {})
            supplier_name = data.get("field1", "")
            reliability_score = data.get("field5", 0)
            delivery_time = data.get("field8", 0)
            risk_level = data.get("field10", "medium")
            
            # Get orders for this supplier
            supplier_orders = [order for order in orders if order.get("data", {}).get("field2") == supplier_name]
            
            # Calculate performance metrics
            on_time_delivery = self._calculate_on_time_delivery(supplier_orders)
            cost_competitiveness = self._calculate_cost_competitiveness(supplier_name, supplier_orders)
            communication_score = self._assess_communication_quality(supplier_orders)
            
            overall_score = (
                reliability_score * 0.3 +
                on_time_delivery * 0.25 +
                cost_competitiveness * 0.2 +
                communication_score * 0.25
            )
            
            performance_analysis["supplier_rankings"].append({
                "supplier": supplier_name,
                "overall_score": overall_score,
                "reliability_score": reliability_score,
                "on_time_delivery": on_time_delivery,
                "cost_competitiveness": cost_competitiveness,
                "communication_score": communication_score,
                "risk_level": risk_level,
                "total_orders": len(supplier_orders),
                "recommendation": self._generate_supplier_recommendation(overall_score, risk_level)
            })
        
        # Sort by overall score
        performance_analysis["supplier_rankings"].sort(key=lambda x: x["overall_score"], reverse=True)
        
        return performance_analysis
    
    def optimize_shipping_routes(self, canvas_state: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize shipping routes and logistics operations"""
        logistics_items = [item for item in canvas_state.get("items", []) if item.get("type") == "logistics"]
        
        optimization = {
            "route_optimizations": [],
            "cost_savings": {},
            "delivery_improvements": {},
            "recommendations": []
        }
        
        # Group shipments by region
        regional_shipments = self._group_shipments_by_region(logistics_items)
        
        for region, shipments in regional_shipments.items():
            if len(shipments) > 1:
                # Calculate consolidation opportunities
                consolidation_savings = self._calculate_consolidation_savings(shipments)
                
                # Calculate route optimization
                optimized_route = self._optimize_delivery_route(shipments)
                
                optimization["route_optimizations"].append({
                    "region": region,
                    "shipments_count": len(shipments),
                    "consolidation_savings": consolidation_savings,
                    "optimized_route": optimized_route,
                    "estimated_savings": consolidation_savings["total_savings"]
                })
        
        return optimization
    
    def predict_demand(self, canvas_state: Dict[str, Any]) -> Dict[str, Any]:
        """Predict future demand based on historical data and trends"""
        inventory_items = [item for item in canvas_state.get("items", []) if item.get("type") == "inventory"]
        orders = [item for item in canvas_state.get("items", []) if item.get("type") == "order"]
        
        demand_forecast = {
            "item_forecasts": [],
            "seasonal_trends": {},
            "market_indicators": {},
            "recommendations": []
        }
        
        for item in inventory_items:
            data = item.get("data", {})
            sku = data.get("field2", "")
            name = item.get("name", "")
            
            # Get historical order data for this item
            item_orders = [order for order in orders if sku in order.get("data", {}).get("field8", [])]
            
            # Calculate demand patterns
            demand_pattern = self._analyze_demand_pattern(item_orders)
            seasonal_factor = self._calculate_seasonal_factor(item_orders)
            trend = self._calculate_demand_trend(item_orders)
            
            # Generate forecast for next 3 months
            forecast = self._generate_demand_forecast(demand_pattern, seasonal_factor, trend)
            
            demand_forecast["item_forecasts"].append({
                "item": name,
                "sku": sku,
                "current_demand_rate": demand_pattern["average_daily"],
                "forecast_3_months": forecast,
                "seasonal_factor": seasonal_factor,
                "trend": trend,
                "confidence_level": demand_pattern["confidence"]
            })
        
        return demand_forecast
    
    def identify_supply_chain_risks(self, canvas_state: Dict[str, Any]) -> Dict[str, Any]:
        """Identify and assess supply chain risks"""
        suppliers = [item for item in canvas_state.get("items", []) if item.get("type") == "supplier"]
        inventory_items = [item for item in canvas_state.get("items", []) if item.get("type") == "inventory"]
        
        risk_assessment = {
            "supplier_risks": [],
            "inventory_risks": [],
            "geopolitical_risks": [],
            "operational_risks": [],
            "mitigation_strategies": []
        }
        
        # Assess supplier risks
        for supplier in suppliers:
            data = supplier.get("data", {})
            supplier_name = data.get("field1", "")
            risk_level = data.get("field10", "medium")
            location = data.get("field3", "")
            certifications = data.get("field4", [])
            
            risk_factors = self._assess_supplier_risk_factors(supplier_name, location, certifications)
            
            risk_assessment["supplier_risks"].append({
                "supplier": supplier_name,
                "risk_level": risk_level,
                "location": location,
                "risk_factors": risk_factors,
                "mitigation_score": self._calculate_mitigation_score(risk_factors)
            })
        
        # Assess inventory risks
        for item in inventory_items:
            data = item.get("data", {})
            current_stock = data.get("field3", 0)
            min_stock = data.get("field4", 0)
            supplier = data.get("field9", "")
            lead_time = data.get("field11", 0)
            
            inventory_risk = self._assess_inventory_risk(current_stock, min_stock, lead_time, supplier)
            
            if inventory_risk["risk_level"] != "low":
                risk_assessment["inventory_risks"].append({
                    "item": item.get("name", ""),
                    "sku": data.get("field2", ""),
                    "risk_level": inventory_risk["risk_level"],
                    "risk_factors": inventory_risk["factors"],
                    "impact": inventory_risk["impact"]
                })
        
        return risk_assessment
    
    def generate_procurement_recommendations(self, canvas_state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate procurement recommendations based on cost, quality, and risk factors"""
        suppliers = [item for item in canvas_state.get("items", []) if item.get("type") == "supplier"]
        inventory_items = [item for item in canvas_state.get("items", []) if item.get("type") == "inventory"]
        
        recommendations = {
            "procurement_strategies": [],
            "supplier_recommendations": [],
            "cost_optimization": {},
            "risk_mitigation": []
        }
        
        # Analyze procurement opportunities
        for item in inventory_items:
            data = item.get("data", {})
            sku = data.get("field2", "")
            name = item.get("name", "")
            current_supplier = data.get("field9", "")
            unit_cost = data.get("field8", 0)
            
            # Find alternative suppliers
            alternative_suppliers = self._find_alternative_suppliers(sku, suppliers)
            
            # Calculate procurement optimization
            optimization = self._calculate_procurement_optimization(
                current_supplier, alternative_suppliers, unit_cost
            )
            
            recommendations["procurement_strategies"].append({
                "item": name,
                "sku": sku,
                "current_supplier": current_supplier,
                "current_cost": unit_cost,
                "optimization_opportunity": optimization,
                "recommended_supplier": optimization.get("recommended_supplier"),
                "potential_savings": optimization.get("savings", 0)
            })
        
        return recommendations
    
    def monitor_compliance(self, canvas_state: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor compliance with regulations and quality standards"""
        suppliers = [item for item in canvas_state.get("items", []) if item.get("type") == "supplier"]
        
        compliance_report = {
            "certification_status": [],
            "regulatory_compliance": [],
            "quality_standards": [],
            "audit_recommendations": []
        }
        
        for supplier in suppliers:
            data = supplier.get("data", {})
            supplier_name = data.get("field1", "")
            certifications = data.get("field4", [])
            location = data.get("field3", "")
            
            # Check certification compliance
            cert_status = self._check_certification_compliance(certifications, location)
            
            # Check regulatory compliance
            regulatory_status = self._check_regulatory_compliance(location, supplier_name)
            
            compliance_report["certification_status"].append({
                "supplier": supplier_name,
                "certifications": certifications,
                "compliance_status": cert_status,
                "expiry_dates": self._get_certification_expiry_dates(certifications),
                "renewal_required": cert_status.get("renewal_required", [])
            })
        
        return compliance_report
    
    def optimize_warehouse_operations(self, canvas_state: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize warehouse operations and storage efficiency"""
        inventory_items = [item for item in canvas_state.get("items", []) if item.get("type") == "inventory"]
        
        warehouse_optimization = {
            "storage_optimization": [],
            "picking_efficiency": {},
            "space_utilization": {},
            "automation_opportunities": []
        }
        
        # Analyze storage patterns
        storage_analysis = self._analyze_storage_patterns(inventory_items)
        
        # Calculate picking efficiency
        picking_optimization = self._optimize_picking_operations(inventory_items)
        
        # Identify automation opportunities
        automation_opportunities = self._identify_automation_opportunities(inventory_items)
        
        warehouse_optimization.update({
            "storage_optimization": storage_analysis,
            "picking_efficiency": picking_optimization,
            "automation_opportunities": automation_opportunities
        })
        
        return warehouse_optimization
    
    def calculate_total_cost_of_ownership(self, canvas_state: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate total cost of ownership for suppliers and products"""
        suppliers = [item for item in canvas_state.get("items", []) if item.get("type") == "supplier"]
        inventory_items = [item for item in canvas_state.get("items", []) if item.get("type") == "inventory"]
        
        tco_analysis = {
            "supplier_tco": [],
            "product_tco": [],
            "hidden_costs": [],
            "optimization_opportunities": []
        }
        
        for supplier in suppliers:
            data = supplier.get("data", {})
            supplier_name = data.get("field1", "")
            
            # Calculate TCO for supplier
            tco = self._calculate_supplier_tco(supplier_name, inventory_items)
            
            tco_analysis["supplier_tco"].append({
                "supplier": supplier_name,
                "total_cost": tco["total_cost"],
                "cost_breakdown": tco["breakdown"],
                "cost_per_unit": tco["cost_per_unit"],
                "recommendations": tco["recommendations"]
            })
        
        return tco_analysis
    
    # Helper methods
    def _calculate_inventory_turnover(self, inventory_items: List[Dict]) -> float:
        """Calculate inventory turnover ratio"""
        if not inventory_items:
            return 0
        
        total_cost = sum(item.get("data", {}).get("field8", 0) * item.get("data", {}).get("field3", 0) for item in inventory_items)
        average_inventory = total_cost / len(inventory_items) if inventory_items else 0
        
        # Simplified calculation - in real implementation, use actual sales data
        return 12.0 if average_inventory > 0 else 0
    
    def _generate_inventory_recommendations(self, analysis: Dict) -> List[str]:
        """Generate inventory management recommendations"""
        recommendations = []
        
        if analysis["low_stock_items"]:
            recommendations.append(f"Immediate reorder required for {len(analysis['low_stock_items'])} items")
        
        if analysis["overstock_items"]:
            recommendations.append(f"Consider reducing stock levels for {len(analysis['overstock_items'])} overstocked items")
        
        if analysis["out_of_stock_items"]:
            recommendations.append(f"Critical: {len(analysis['out_of_stock_items'])} items are out of stock")
        
        return recommendations
    
    def _estimate_demand_rate(self, sku: str, current_stock: int) -> float:
        """Estimate demand rate for an item (simplified implementation)"""
        # In real implementation, use historical sales data
        # For now, use a simple heuristic based on stock levels
        if current_stock > 100:
            return 5.0  # High demand
        elif current_stock > 50:
            return 2.0  # Medium demand
        else:
            return 1.0  # Low demand
    
    def _calculate_safety_stock(self, demand_rate: float, lead_time: int) -> int:
        """Calculate safety stock based on demand variability and lead time"""
        # Simplified safety stock calculation
        # In real implementation, use statistical methods
        return int(demand_rate * lead_time * 0.2)  # 20% of lead time demand
    
    def _calculate_eoq(self, demand_rate: float, unit_cost: float) -> int:
        """Calculate Economic Order Quantity"""
        # Simplified EOQ calculation
        # In real implementation, include ordering costs and holding costs
        annual_demand = demand_rate * 365
        ordering_cost = 50  # Simplified assumption
        holding_cost = unit_cost * 0.1  # 10% of unit cost
        
        if holding_cost > 0:
            return int(math.sqrt((2 * annual_demand * ordering_cost) / holding_cost))
        return 100  # Default fallback
    
    def _calculate_on_time_delivery(self, orders: List[Dict]) -> float:
        """Calculate on-time delivery rate for a supplier"""
        if not orders:
            return 0.0
        
        on_time_count = 0
        for order in orders:
            status = order.get("data", {}).get("field5", "")
            if status in ["delivered", "shipped"]:
                on_time_count += 1
        
        return (on_time_count / len(orders)) * 100 if orders else 0.0
    
    def _calculate_cost_competitiveness(self, supplier_name: str, orders: List[Dict]) -> float:
        """Calculate cost competitiveness score"""
        if not orders:
            return 50.0  # Neutral score
        
        # Simplified calculation - in real implementation, compare with market rates
        total_cost = sum(order.get("data", {}).get("field6", 0) for order in orders)
        average_cost = total_cost / len(orders) if orders else 0
        
        # Score based on cost (lower is better)
        if average_cost < 1000:
            return 90.0
        elif average_cost < 5000:
            return 70.0
        else:
            return 50.0
    
    def _assess_communication_quality(self, orders: List[Dict]) -> float:
        """Assess communication quality with supplier"""
        # Simplified assessment - in real implementation, analyze communication logs
        return 75.0  # Default good score
    
    def _generate_supplier_recommendation(self, overall_score: float, risk_level: str) -> str:
        """Generate supplier recommendation based on performance"""
        if overall_score >= 80 and risk_level == "low":
            return "Excellent supplier - maintain relationship"
        elif overall_score >= 60:
            return "Good supplier - monitor performance"
        elif overall_score >= 40:
            return "Needs improvement - consider alternatives"
        else:
            return "Poor performance - consider replacement"
    
    def _group_shipments_by_region(self, logistics_items: List[Dict]) -> Dict[str, List[Dict]]:
        """Group shipments by destination region"""
        regional_shipments = {}
        
        for item in logistics_items:
            data = item.get("data", {})
            destination = data.get("field4", "")
            region = destination.split(",")[-1].strip() if destination else "Unknown"
            
            if region not in regional_shipments:
                regional_shipments[region] = []
            regional_shipments[region].append(item)
        
        return regional_shipments
    
    def _calculate_consolidation_savings(self, shipments: List[Dict]) -> Dict[str, Any]:
        """Calculate potential savings from shipment consolidation"""
        total_shipments = len(shipments)
        total_cost = sum(item.get("data", {}).get("field9", 0) for item in shipments)
        
        # Simplified consolidation calculation
        consolidation_savings = total_cost * 0.15  # 15% savings from consolidation
        
        return {
            "total_shipments": total_shipments,
            "current_cost": total_cost,
            "consolidated_cost": total_cost - consolidation_savings,
            "total_savings": consolidation_savings,
            "savings_percentage": 15.0
        }
    
    def _optimize_delivery_route(self, shipments: List[Dict]) -> Dict[str, Any]:
        """Optimize delivery route for shipments"""
        # Simplified route optimization
        return {
            "optimized_route": "Direct delivery with consolidation",
            "estimated_time_savings": "2-3 days",
            "cost_reduction": "15%"
        }
    
    def _analyze_demand_pattern(self, orders: List[Dict]) -> Dict[str, Any]:
        """Analyze demand patterns from historical orders"""
        if not orders:
            return {"average_daily": 1.0, "confidence": 0.5}
        
        # Simplified analysis
        return {
            "average_daily": 2.5,
            "confidence": 0.8,
            "seasonality": "moderate",
            "trend": "stable"
        }
    
    def _calculate_seasonal_factor(self, orders: List[Dict]) -> float:
        """Calculate seasonal factor for demand"""
        # Simplified seasonal calculation
        return 1.2  # 20% seasonal increase
    
    def _calculate_demand_trend(self, orders: List[Dict]) -> str:
        """Calculate demand trend"""
        # Simplified trend calculation
        return "increasing"
    
    def _generate_demand_forecast(self, demand_pattern: Dict, seasonal_factor: float, trend: str) -> Dict[str, Any]:
        """Generate demand forecast for next 3 months"""
        base_demand = demand_pattern["average_daily"]
        
        return {
            "month_1": int(base_demand * seasonal_factor * 30),
            "month_2": int(base_demand * seasonal_factor * 1.1 * 30),
            "month_3": int(base_demand * seasonal_factor * 1.2 * 30),
            "trend": trend
        }
    
    def _assess_supplier_risk_factors(self, supplier_name: str, location: str, certifications: List[str]) -> List[str]:
        """Assess risk factors for a supplier"""
        risk_factors = []
        
        if not certifications:
            risk_factors.append("No certifications")
        
        if "high-risk" in location.lower():
            risk_factors.append("High-risk location")
        
        if len(certifications) < 2:
            risk_factors.append("Limited certifications")
        
        return risk_factors
    
    def _calculate_mitigation_score(self, risk_factors: List[str]) -> float:
        """Calculate mitigation score based on risk factors"""
        if not risk_factors:
            return 100.0
        
        return max(0, 100 - len(risk_factors) * 20)
    
    def _assess_inventory_risk(self, current_stock: int, min_stock: int, lead_time: int, supplier: str) -> Dict[str, Any]:
        """Assess inventory risk for an item"""
        if current_stock == 0:
            return {
                "risk_level": "critical",
                "factors": ["Out of stock"],
                "impact": "Production halt"
            }
        elif current_stock <= min_stock:
            return {
                "risk_level": "high",
                "factors": ["Below minimum stock"],
                "impact": "Potential stockout"
            }
        else:
            return {
                "risk_level": "low",
                "factors": [],
                "impact": "Minimal"
            }
    
    def _find_alternative_suppliers(self, sku: str, suppliers: List[Dict]) -> List[Dict]:
        """Find alternative suppliers for a product"""
        alternatives = []
        
        for supplier in suppliers:
            data = supplier.get("data", {})
            products = data.get("field7", [])
            
            if sku in products or any(sku.lower() in product.lower() for product in products):
                alternatives.append({
                    "supplier": data.get("field1", ""),
                    "reliability": data.get("field5", 0),
                    "delivery_time": data.get("field8", 0),
                    "risk_level": data.get("field10", "medium")
                })
        
        return alternatives
    
    def _calculate_procurement_optimization(self, current_supplier: str, alternatives: List[Dict], current_cost: float) -> Dict[str, Any]:
        """Calculate procurement optimization opportunities"""
        if not alternatives:
            return {"savings": 0, "recommended_supplier": current_supplier}
        
        # Find best alternative
        best_alternative = max(alternatives, key=lambda x: x["reliability"])
        
        # Simplified cost calculation
        potential_savings = current_cost * 0.1  # 10% potential savings
        
        return {
            "savings": potential_savings,
            "recommended_supplier": best_alternative["supplier"],
            "reliability_improvement": best_alternative["reliability"] - 70  # Assuming current is 70
        }
    
    def _check_certification_compliance(self, certifications: List[str], location: str) -> Dict[str, Any]:
        """Check certification compliance status"""
        required_certs = ["ISO 9001", "ISO 14001"]
        missing_certs = [cert for cert in required_certs if cert not in certifications]
        
        return {
            "compliant": len(missing_certs) == 0,
            "missing_certifications": missing_certs,
            "renewal_required": []
        }
    
    def _check_regulatory_compliance(self, location: str, supplier_name: str) -> Dict[str, Any]:
        """Check regulatory compliance"""
        # Simplified compliance check
        return {
            "compliant": True,
            "regulations": ["Environmental", "Labor", "Safety"],
            "last_audit": "2024-01-15"
        }
    
    def _get_certification_expiry_dates(self, certifications: List[str]) -> Dict[str, str]:
        """Get certification expiry dates"""
        # Simplified expiry dates
        expiry_dates = {}
        for cert in certifications:
            expiry_dates[cert] = "2025-12-31"  # Default expiry
        
        return expiry_dates
    
    def _analyze_storage_patterns(self, inventory_items: List[Dict]) -> List[Dict]:
        """Analyze storage patterns for optimization"""
        return [
            {
                "optimization": "ABC Analysis",
                "description": "Classify items by value and frequency",
                "potential_savings": "15%"
            }
        ]
    
    def _optimize_picking_operations(self, inventory_items: List[Dict]) -> Dict[str, Any]:
        """Optimize picking operations"""
        return {
            "current_efficiency": "75%",
            "optimized_efficiency": "90%",
            "improvement": "20%"
        }
    
    def _identify_automation_opportunities(self, inventory_items: List[Dict]) -> List[Dict]:
        """Identify automation opportunities"""
        return [
            {
                "opportunity": "Automated picking",
                "description": "Implement robotic picking for high-volume items",
                "investment": "$50,000",
                "roi": "18 months"
            }
        ]
    
    def _calculate_supplier_tco(self, supplier_name: str, inventory_items: List[Dict]) -> Dict[str, Any]:
        """Calculate total cost of ownership for a supplier"""
        # Simplified TCO calculation
        return {
            "total_cost": 100000,
            "breakdown": {
                "direct_costs": 80000,
                "indirect_costs": 15000,
                "risk_costs": 5000
            },
            "cost_per_unit": 10.0,
            "recommendations": ["Negotiate better terms", "Improve quality"]
        }
