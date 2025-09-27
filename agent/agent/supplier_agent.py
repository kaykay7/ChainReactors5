"""
🏭 SUPPLIER MANAGEMENT AGENT
Specialized agent for supplier evaluation, performance tracking, and procurement optimization.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

class SupplierAgent:
    """Specialized agent for supplier management and optimization."""
    
    def __init__(self, agent_id: str = "supplier_agent"):
        self.agent_id = agent_id
        self.capabilities = [
            "supplier_performance_analysis",
            "risk_assessment",
            "cost_optimization",
            "supplier_selection",
            "contract_management",
            "quality_monitoring"
        ]
    
    def analyze_supplier_performance(self, supplier_data: List[Dict]) -> Dict[str, Any]:
        """Analyze supplier performance across multiple metrics."""
        performance_analysis = {}
        
        for supplier in supplier_data:
            supplier_id = supplier.get('id')
            
            # Calculate performance scores
            delivery_score = self._calculate_delivery_score(supplier)
            quality_score = self._calculate_quality_score(supplier)
            cost_score = self._calculate_cost_score(supplier)
            reliability_score = supplier.get('reliability_score', 0)
            
            # Overall performance score (weighted average)
            overall_score = (
                delivery_score * 0.3 +
                quality_score * 0.3 +
                cost_score * 0.2 +
                reliability_score * 0.2
            )
            
            performance_analysis[supplier_id] = {
                "supplier_name": supplier.get('name'),
                "overall_score": round(overall_score, 2),
                "delivery_score": delivery_score,
                "quality_score": quality_score,
                "cost_score": cost_score,
                "reliability_score": reliability_score,
                "performance_tier": self._categorize_performance(overall_score),
                "recommendations": self._generate_supplier_recommendations(supplier, overall_score)
            }
        
        return {"supplier_performance": performance_analysis}
    
    def assess_supplier_risks(self, supplier_data: List[Dict]) -> Dict[str, Any]:
        """Assess supplier risks and vulnerabilities."""
        risk_assessment = {}
        
        for supplier in supplier_data:
            supplier_id = supplier.get('id')
            risks = []
            risk_score = 0
            
            # Geographic risk
            location = supplier.get('location', '')
            if location in ['Asia Pacific', 'Europe']:  # Example risk factors
                risks.append({
                    "type": "geographic",
                    "description": "International supplier with potential shipping delays",
                    "severity": "medium"
                })
                risk_score += 0.3
            
            # Single source risk
            if supplier.get('is_sole_supplier', False):
                risks.append({
                    "type": "single_source",
                    "description": "Sole supplier for critical components",
                    "severity": "high"
                })
                risk_score += 0.5
            
            # Financial risk
            reliability = supplier.get('reliability_score', 0)
            if reliability < 70:
                risks.append({
                    "type": "financial",
                    "description": "Low reliability score indicates potential financial instability",
                    "severity": "high" if reliability < 50 else "medium"
                })
                risk_score += 0.4 if reliability < 50 else 0.2
            
            # Compliance risk
            certifications = supplier.get('certifications', '')
            if 'ISO 9001' not in certifications:
                risks.append({
                    "type": "compliance",
                    "description": "Missing key quality certifications",
                    "severity": "medium"
                })
                risk_score += 0.2
            
            risk_assessment[supplier_id] = {
                "supplier_name": supplier.get('name'),
                "risk_score": round(risk_score, 2),
                "risk_level": "high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low",
                "risks": risks,
                "mitigation_strategies": self._generate_mitigation_strategies(risks)
            }
        
        return {"supplier_risks": risk_assessment}
    
    def optimize_procurement(self, supplier_data: List[Dict], requirements: Dict) -> Dict[str, Any]:
        """Optimize procurement decisions based on supplier performance and requirements."""
        procurement_recommendations = []
        
        for requirement in requirements.get('items', []):
            item_name = requirement.get('item_name')
            quantity = requirement.get('quantity', 1)
            urgency = requirement.get('urgency', 'medium')
            
            # Find suitable suppliers
            suitable_suppliers = []
            for supplier in supplier_data:
                if self._supplier_can_fulfill(supplier, requirement):
                    score = self._calculate_procurement_score(supplier, requirement)
                    suitable_suppliers.append({
                        "supplier_id": supplier.get('id'),
                        "supplier_name": supplier.get('name'),
                        "score": score,
                        "delivery_time": supplier.get('delivery_time', 0),
                        "cost": supplier.get('unit_cost', 0) * quantity,
                        "reliability": supplier.get('reliability_score', 0)
                    })
            
            # Sort by score and urgency
            suitable_suppliers.sort(key=lambda x: x['score'], reverse=True)
            
            procurement_recommendations.append({
                "item_name": item_name,
                "quantity": quantity,
                "urgency": urgency,
                "recommended_suppliers": suitable_suppliers[:3],  # Top 3 options
                "recommendation": self._generate_procurement_recommendation(suitable_suppliers, urgency)
            })
        
        return {"procurement_recommendations": procurement_recommendations}
    
    def calculate_total_cost_of_ownership(self, supplier_data: List[Dict], item_requirements: List[Dict]) -> Dict[str, Any]:
        """Calculate total cost of ownership for different supplier options."""
        tco_analysis = {}
        
        for requirement in item_requirements:
            item_name = requirement.get('item_name')
            quantity = requirement.get('quantity', 1)
            
            supplier_tcos = []
            for supplier in supplier_data:
                if self._supplier_can_fulfill(supplier, requirement):
                    tco = self._calculate_tco(supplier, requirement)
                    supplier_tcos.append({
                        "supplier_id": supplier.get('id'),
                        "supplier_name": supplier.get('name'),
                        "tco": tco,
                        "breakdown": self._get_tco_breakdown(supplier, requirement)
                    })
            
            # Sort by TCO
            supplier_tcos.sort(key=lambda x: x['tco'])
            
            tco_analysis[item_name] = {
                "quantity": quantity,
                "supplier_options": supplier_tcos,
                "best_option": supplier_tcos[0] if supplier_tcos else None,
                "cost_savings": self._calculate_potential_savings(supplier_tcos)
            }
        
        return {"tco_analysis": tco_analysis}
    
    def _calculate_delivery_score(self, supplier: Dict) -> float:
        """Calculate delivery performance score."""
        delivery_time = supplier.get('delivery_time', 0)
        on_time_delivery = supplier.get('on_time_delivery_rate', 100)
        
        # Score based on delivery time and reliability
        time_score = max(0, 100 - delivery_time)  # Shorter delivery = higher score
        reliability_score = on_time_delivery
        
        return (time_score * 0.6 + reliability_score * 0.4) / 100
    
    def _calculate_quality_score(self, supplier: Dict) -> float:
        """Calculate quality performance score."""
        certifications = supplier.get('certifications', '')
        quality_score = 50  # Base score
        
        # Add points for certifications
        if 'ISO 9001' in certifications:
            quality_score += 20
        if 'FDA Certified' in certifications:
            quality_score += 15
        if 'ISO 14001' in certifications:
            quality_score += 10
        
        return min(100, quality_score) / 100
    
    def _calculate_cost_score(self, supplier: Dict) -> float:
        """Calculate cost competitiveness score."""
        unit_cost = supplier.get('unit_cost', 0)
        if unit_cost == 0:
            return 0.5  # Neutral score if no cost data
        
        # This would typically compare against market average
        # For now, use a simple scoring system
        if unit_cost < 10:
            return 1.0
        elif unit_cost < 25:
            return 0.8
        elif unit_cost < 50:
            return 0.6
        else:
            return 0.4
    
    def _categorize_performance(self, score: float) -> str:
        """Categorize supplier performance."""
        if score >= 0.9:
            return "excellent"
        elif score >= 0.8:
            return "good"
        elif score >= 0.6:
            return "average"
        else:
            return "poor"
    
    def _generate_supplier_recommendations(self, supplier: Dict, score: float) -> List[str]:
        """Generate recommendations for supplier improvement."""
        recommendations = []
        
        if score < 0.6:
            recommendations.append("Consider finding alternative suppliers")
        
        if supplier.get('reliability_score', 0) < 70:
            recommendations.append("Improve delivery reliability")
        
        if 'ISO 9001' not in supplier.get('certifications', ''):
            recommendations.append("Obtain ISO 9001 certification")
        
        if supplier.get('delivery_time', 0) > 14:
            recommendations.append("Reduce delivery lead times")
        
        return recommendations
    
    def _generate_mitigation_strategies(self, risks: List[Dict]) -> List[str]:
        """Generate risk mitigation strategies."""
        strategies = []
        
        for risk in risks:
            if risk['type'] == 'geographic':
                strategies.append("Diversify supplier base across multiple regions")
            elif risk['type'] == 'single_source':
                strategies.append("Identify and qualify backup suppliers")
            elif risk['type'] == 'financial':
                strategies.append("Monitor supplier financial health regularly")
            elif risk['type'] == 'compliance':
                strategies.append("Require specific certifications in contracts")
        
        return strategies
    
    def _supplier_can_fulfill(self, supplier: Dict, requirement: Dict) -> bool:
        """Check if supplier can fulfill the requirement."""
        # Simple check - in reality, this would be more complex
        products = supplier.get('products', '').lower()
        item_name = requirement.get('item_name', '').lower()
        
        return item_name in products or 'general' in products
    
    def _calculate_procurement_score(self, supplier: Dict, requirement: Dict) -> float:
        """Calculate procurement score for a supplier."""
        urgency = requirement.get('urgency', 'medium')
        
        # Base score from supplier performance
        reliability = supplier.get('reliability_score', 0) / 100
        delivery_time = supplier.get('delivery_time', 0)
        
        # Adjust for urgency
        if urgency == 'urgent':
            delivery_weight = 0.7
            reliability_weight = 0.3
        else:
            delivery_weight = 0.4
            reliability_weight = 0.6
        
        # Calculate score
        delivery_score = max(0, 1 - (delivery_time / 30))  # Normalize delivery time
        score = (delivery_score * delivery_weight + reliability * reliability_weight)
        
        return score
    
    def _generate_procurement_recommendation(self, suppliers: List[Dict], urgency: str) -> str:
        """Generate procurement recommendation."""
        if not suppliers:
            return "No suitable suppliers found"
        
        best_supplier = suppliers[0]
        
        if urgency == 'urgent':
            return f"Use {best_supplier['supplier_name']} for fastest delivery"
        else:
            return f"Use {best_supplier['supplier_name']} for best overall performance"
    
    def _calculate_tco(self, supplier: Dict, requirement: Dict) -> float:
        """Calculate total cost of ownership."""
        quantity = requirement.get('quantity', 1)
        unit_cost = supplier.get('unit_cost', 0)
        delivery_time = supplier.get('delivery_time', 0)
        
        # Basic TCO calculation
        product_cost = unit_cost * quantity
        shipping_cost = supplier.get('shipping_cost', 0)
        holding_cost = product_cost * 0.1 * (delivery_time / 365)  # 10% annual holding cost
        
        return product_cost + shipping_cost + holding_cost
    
    def _get_tco_breakdown(self, supplier: Dict, requirement: Dict) -> Dict[str, float]:
        """Get detailed TCO breakdown."""
        quantity = requirement.get('quantity', 1)
        unit_cost = supplier.get('unit_cost', 0)
        
        return {
            "product_cost": unit_cost * quantity,
            "shipping_cost": supplier.get('shipping_cost', 0),
            "holding_cost": unit_cost * quantity * 0.1 * (supplier.get('delivery_time', 0) / 365),
            "total": self._calculate_tco(supplier, requirement)
        }
    
    def _calculate_potential_savings(self, supplier_options: List[Dict]) -> Dict[str, float]:
        """Calculate potential cost savings."""
        if len(supplier_options) < 2:
            return {"savings": 0, "percentage": 0}
        
        best_tco = supplier_options[0]['tco']
        worst_tco = supplier_options[-1]['tco']
        
        savings = worst_tco - best_tco
        percentage = (savings / worst_tco) * 100 if worst_tco > 0 else 0
        
        return {
            "savings": round(savings, 2),
            "percentage": round(percentage, 1)
        }
    
    def collaborate_with_inventory_agent(self, supplier_recommendations: Dict) -> Dict[str, Any]:
        """Send supplier recommendations to inventory agent."""
        return {
            "request_type": "supplier_recommendations",
            "target_agent": "inventory_agent",
            "data": supplier_recommendations,
            "request_id": f"supplier_{datetime.now().isoformat()}"
        }
    
    def collaborate_with_logistics_agent(self, procurement_data: Dict) -> Dict[str, Any]:
        """Send procurement data to logistics agent for shipping optimization."""
        return {
            "request_type": "shipping_optimization",
            "target_agent": "logistics_agent",
            "data": procurement_data,
            "request_id": f"supplier_{datetime.now().isoformat()}"
        }
