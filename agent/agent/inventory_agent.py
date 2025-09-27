"""
🧮 INVENTORY MANAGEMENT AGENT
Specialized agent for inventory optimization, stock management, and reorder point calculations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

class InventoryAgent:
    """Specialized agent for inventory management and optimization."""
    
    def __init__(self, agent_id: str = "inventory_agent", memory_manager=None):
        self.agent_id = agent_id
        self.memory_manager = memory_manager
        self.capabilities = [
            "stock_level_analysis",
            "reorder_point_calculation", 
            "safety_stock_optimization",
            "abc_analysis",
            "inventory_turnover_analysis",
            "stockout_prediction"
        ]
    
    def analyze_stock_levels(self, inventory_data: List[Dict]) -> Dict[str, Any]:
        """Analyze current stock levels and identify issues."""
        # Get historical context from memory
        historical_context = self._get_historical_context()
        
        analysis = {
            "low_stock_items": [],
            "out_of_stock_items": [],
            "overstocked_items": [],
            "critical_items": [],
            "recommendations": [],
            "historical_insights": historical_context
        }
        
        for item in inventory_data:
            current_stock = item.get('current_stock', 0)
            min_stock = item.get('min_stock', 0)
            max_stock = item.get('max_stock', 0)
            reorder_point = item.get('reorder_point', 0)
            
            # Low stock analysis
            if current_stock <= reorder_point:
                analysis["low_stock_items"].append({
                    "item_id": item.get('id'),
                    "name": item.get('name'),
                    "current_stock": current_stock,
                    "reorder_point": reorder_point,
                    "urgency": "high" if current_stock <= min_stock else "medium"
                })
            
            # Out of stock
            if current_stock == 0:
                analysis["out_of_stock_items"].append({
                    "item_id": item.get('id'),
                    "name": item.get('name'),
                    "impact": "critical"
                })
            
            # Overstocked items
            if current_stock > max_stock * 1.2:  # 20% over max
                analysis["overstocked_items"].append({
                    "item_id": item.get('id'),
                    "name": item.get('name'),
                    "current_stock": current_stock,
                    "max_stock": max_stock,
                    "excess": current_stock - max_stock
                })
        
        return analysis
    
    def calculate_reorder_points(self, inventory_data: List[Dict], demand_forecast: Dict = None) -> Dict[str, Any]:
        """Calculate optimal reorder points based on demand patterns."""
        recommendations = []
        
        for item in inventory_data:
            # Get historical demand data
            historical_demand = item.get('historical_demand', [])
            lead_time = item.get('lead_time', 7)  # days
            safety_factor = item.get('safety_factor', 1.5)
            
            if historical_demand:
                avg_daily_demand = sum(historical_demand) / len(historical_demand)
                demand_variance = self._calculate_variance(historical_demand)
                
                # Reorder point = (Average Daily Demand × Lead Time) + Safety Stock
                safety_stock = safety_factor * (demand_variance ** 0.5) * (lead_time ** 0.5)
                reorder_point = (avg_daily_demand * lead_time) + safety_stock
                
                recommendations.append({
                    "item_id": item.get('id'),
                    "name": item.get('name'),
                    "current_reorder_point": item.get('reorder_point', 0),
                    "recommended_reorder_point": int(reorder_point),
                    "safety_stock": int(safety_stock),
                    "confidence": "high" if len(historical_demand) > 30 else "medium"
                })
        
        return {"reorder_recommendations": recommendations}
    
    def predict_stockouts(self, inventory_data: List[Dict], demand_forecast: Dict = None) -> Dict[str, Any]:
        """Predict potential stockouts based on current trends."""
        predictions = []
        
        for item in inventory_data:
            current_stock = item.get('current_stock', 0)
            daily_consumption = item.get('daily_consumption', 0)
            
            if daily_consumption > 0:
                days_until_stockout = current_stock / daily_consumption
                
                predictions.append({
                    "item_id": item.get('id'),
                    "name": item.get('name'),
                    "current_stock": current_stock,
                    "days_until_stockout": round(days_until_stockout, 1),
                    "risk_level": "critical" if days_until_stockout < 3 else 
                               "high" if days_until_stockout < 7 else 
                               "medium" if days_until_stockout < 14 else "low"
                })
        
        return {"stockout_predictions": predictions}
    
    def perform_abc_analysis(self, inventory_data: List[Dict]) -> Dict[str, Any]:
        """Perform ABC analysis to categorize inventory by value."""
        # Calculate total value for each item
        items_with_value = []
        for item in inventory_data:
            current_stock = item.get('current_stock', 0)
            unit_cost = item.get('unit_cost', 0)
            total_value = current_stock * unit_cost
            items_with_value.append({
                **item,
                'total_value': total_value
            })
        
        # Sort by total value (descending)
        items_with_value.sort(key=lambda x: x['total_value'], reverse=True)
        
        # Calculate cumulative percentages
        total_inventory_value = sum(item['total_value'] for item in items_with_value)
        cumulative_percentage = 0
        
        abc_categories = {"A": [], "B": [], "C": []}
        
        for item in items_with_value:
            item_value_percentage = (item['total_value'] / total_inventory_value) * 100
            cumulative_percentage += item_value_percentage
            
            if cumulative_percentage <= 80:
                category = "A"
            elif cumulative_percentage <= 95:
                category = "B"
            else:
                category = "C"
            
            abc_categories[category].append({
                "item_id": item.get('id'),
                "name": item.get('name'),
                "total_value": item['total_value'],
                "percentage": round(item_value_percentage, 2)
            })
        
        return {"abc_analysis": abc_categories}
    
    def _calculate_variance(self, data: List[float]) -> float:
        """Calculate variance of a dataset."""
        if len(data) < 2:
            return 0
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        return variance
    
    def collaborate_with_forecasting_agent(self, inventory_data: List[Dict]) -> Dict[str, Any]:
        """Request demand forecasting from the forecasting agent."""
        # This would be called by the orchestrator agent
        return {
            "request_type": "demand_forecast",
            "target_agent": "forecasting_agent",
            "data": inventory_data,
            "request_id": f"inventory_{datetime.now().isoformat()}"
        }
    
    def collaborate_with_supplier_agent(self, low_stock_items: List[Dict]) -> Dict[str, Any]:
        """Request supplier recommendations from the supplier agent."""
        # Store collaboration request in memory
        if self.memory_manager:
            self.memory_manager.store_collaboration_event(
                self.agent_id, "supplier_agent", "supplier_recommendations_request", 
                {"low_stock_items": low_stock_items}
            )
        
        return {
            "request_type": "supplier_recommendations",
            "target_agent": "supplier_agent", 
            "data": low_stock_items,
            "request_id": f"inventory_{datetime.now().isoformat()}"
        }
    
    def _get_historical_context(self) -> Dict[str, Any]:
        """Get historical context from memory."""
        if not self.memory_manager:
            return {}
        
        # Get recent inventory analysis patterns
        recent_analyses = self.memory_manager.retrieve_agent_memory(
            self.agent_id, "inventory analysis stock levels patterns", limit=5
        )
        
        # Get learning insights
        learning_insights = self.memory_manager.get_agent_learning_history(self.agent_id)
        
        return {
            "recent_patterns": recent_analyses,
            "learning_insights": learning_insights
        }
    
    def store_analysis_results(self, analysis_results: Dict[str, Any], 
                              recommendations: List[str] = None) -> str:
        """Store analysis results in memory for future reference."""
        if not self.memory_manager:
            return "Memory manager not available"
        
        return self.memory_manager.store_analysis_results(
            self.agent_id, "inventory_analysis", analysis_results, recommendations
        )
    
    def get_historical_insights(self, insight_type: str) -> List[Dict[str, Any]]:
        """Get historical insights of a specific type."""
        if not self.memory_manager:
            return []
        
        return self.memory_manager.get_historical_insights(self.agent_id, insight_type)
