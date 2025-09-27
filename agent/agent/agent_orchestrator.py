"""
🎯 AGENT ORCHESTRATOR
Coordinates specialized agents and manages agent-to-agent communication.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import asyncio
from dataclasses import dataclass

from .inventory_agent import InventoryAgent
from .forecasting_agent import ForecastingAgent
from .supplier_agent import SupplierAgent
from .memory_manager import AgentMemoryManager

@dataclass
class AgentMessage:
    """Message structure for agent-to-agent communication."""
    sender: str
    recipient: str
    message_type: str
    data: Dict[str, Any]
    timestamp: datetime
    request_id: str

class AgentOrchestrator:
    """Orchestrates specialized agents and manages collaboration."""
    
    def __init__(self, memory_dir: str = "./agent_memory"):
        # Initialize memory manager
        self.memory_manager = AgentMemoryManager(memory_dir)
        
        # Initialize agents with memory manager
        self.agents = {
            "inventory_agent": InventoryAgent(memory_manager=self.memory_manager),
            "forecasting_agent": ForecastingAgent(memory_manager=self.memory_manager),
            "supplier_agent": SupplierAgent(memory_manager=self.memory_manager)
        }
        self.message_queue = []
        self.conversation_context = {}
    
    async def process_user_request(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user request and coordinate appropriate agents."""
        # Store user interaction in memory
        self.memory_manager.store_agent_interaction(
            "orchestrator", "user_request", context, user_input
        )
        
        # Analyze user intent
        intent = self._analyze_intent(user_input)
        
        # Route to appropriate agents
        if intent["primary_agent"] == "inventory_agent":
            return await self._handle_inventory_request(user_input, context, intent)
        elif intent["primary_agent"] == "forecasting_agent":
            return await self._handle_forecasting_request(user_input, context, intent)
        elif intent["primary_agent"] == "supplier_agent":
            return await self._handle_supplier_request(user_input, context, intent)
        else:
            return await self._handle_complex_request(user_input, context, intent)
    
    async def _handle_inventory_request(self, user_input: str, context: Dict[str, Any], intent: Dict) -> Dict[str, Any]:
        """Handle inventory-related requests with potential agent collaboration."""
        inventory_agent = self.agents["inventory_agent"]
        
        # Get inventory data from context
        inventory_data = context.get("inventory_data", [])
        
        # Primary inventory analysis
        inventory_analysis = inventory_agent.analyze_stock_levels(inventory_data)
        
        # Check if forecasting collaboration is needed
        if intent.get("needs_forecasting", False):
            # Request demand forecast
            forecast_request = inventory_agent.collaborate_with_forecasting_agent(inventory_data)
            self.message_queue.append(forecast_request)
            
            # Get forecast data (in real implementation, this would be async)
            forecast_data = await self._get_forecast_data(inventory_data)
            
            # Update reorder points with forecast data
            reorder_analysis = inventory_agent.calculate_reorder_points(inventory_data, forecast_data)
            inventory_analysis["reorder_analysis"] = reorder_analysis
        
        # Check if supplier collaboration is needed
        if intent.get("needs_supplier_recommendations", False):
            low_stock_items = inventory_analysis.get("low_stock_items", [])
            if low_stock_items:
                # Request supplier recommendations
                supplier_request = inventory_agent.collaborate_with_supplier_agent(low_stock_items)
                self.message_queue.append(supplier_request)
                
                # Get supplier recommendations
                supplier_data = context.get("supplier_data", [])
                supplier_agent = self.agents["supplier_agent"]
                procurement_recs = supplier_agent.optimize_procurement(supplier_data, {
                    "items": [{"item_name": item["name"], "quantity": item.get("reorder_quantity", 100), "urgency": "medium"} 
                             for item in low_stock_items]
                })
                inventory_analysis["supplier_recommendations"] = procurement_recs
        
        return {
            "response_type": "inventory_analysis",
            "data": inventory_analysis,
            "collaboration_summary": self._get_collaboration_summary()
        }
    
    async def _handle_forecasting_request(self, user_input: str, context: Dict[str, Any], intent: Dict) -> Dict[str, Any]:
        """Handle forecasting requests with potential agent collaboration."""
        forecasting_agent = self.agents["forecasting_agent"]
        
        # Get historical data
        historical_data = context.get("historical_demand_data", [])
        
        # Generate forecasts
        forecasts = forecasting_agent.forecast_demand(historical_data)
        
        # Check if inventory collaboration is needed
        if intent.get("needs_inventory_integration", False):
            # Send forecast data to inventory agent
            inventory_request = forecasting_agent.collaborate_with_inventory_agent(forecasts)
            self.message_queue.append(inventory_request)
        
        return {
            "response_type": "demand_forecast",
            "data": forecasts,
            "collaboration_summary": self._get_collaboration_summary()
        }
    
    async def _handle_supplier_request(self, user_input: str, context: Dict[str, Any], intent: Dict) -> Dict[str, Any]:
        """Handle supplier-related requests with potential agent collaboration."""
        supplier_agent = self.agents["supplier_agent"]
        
        # Get supplier data
        supplier_data = context.get("supplier_data", [])
        
        # Primary supplier analysis
        performance_analysis = supplier_agent.analyze_supplier_performance(supplier_data)
        risk_assessment = supplier_agent.assess_supplier_risks(supplier_data)
        
        # Check if logistics collaboration is needed
        if intent.get("needs_logistics_optimization", False):
            # Send procurement data to logistics agent
            logistics_request = supplier_agent.collaborate_with_logistics_agent({
                "supplier_data": supplier_data,
                "performance_analysis": performance_analysis
            })
            self.message_queue.append(logistics_request)
        
        return {
            "response_type": "supplier_analysis",
            "data": {
                "performance": performance_analysis,
                "risks": risk_assessment
            },
            "collaboration_summary": self._get_collaboration_summary()
        }
    
    async def _handle_complex_request(self, user_input: str, context: Dict[str, Any], intent: Dict) -> Dict[str, Any]:
        """Handle complex requests requiring multiple agents."""
        # This is where the magic happens - multi-agent collaboration!
        
        # Example: "Optimize our supply chain for the next quarter"
        results = {}
        
        # Step 1: Get demand forecast
        forecasting_agent = self.agents["forecasting_agent"]
        historical_data = context.get("historical_demand_data", [])
        forecasts = forecasting_agent.forecast_demand(historical_data)
        results["forecast"] = forecasts
        
        # Step 2: Analyze current inventory with forecast data
        inventory_agent = self.agents["inventory_agent"]
        inventory_data = context.get("inventory_data", [])
        inventory_analysis = inventory_agent.analyze_stock_levels(inventory_data)
        reorder_analysis = inventory_agent.calculate_reorder_points(inventory_data, forecasts)
        results["inventory"] = {**inventory_analysis, **reorder_analysis}
        
        # Step 3: Get supplier recommendations for low stock items
        supplier_agent = self.agents["supplier_agent"]
        low_stock_items = inventory_analysis.get("low_stock_items", [])
        if low_stock_items:
            supplier_data = context.get("supplier_data", [])
            procurement_recs = supplier_agent.optimize_procurement(supplier_data, {
                "items": [{"item_name": item["name"], "quantity": item.get("reorder_quantity", 100), "urgency": "medium"} 
                         for item in low_stock_items]
            })
            results["supplier_recommendations"] = procurement_recs
        
        # Step 4: Generate comprehensive recommendations
        recommendations = self._generate_comprehensive_recommendations(results)
        
        return {
            "response_type": "comprehensive_analysis",
            "data": results,
            "recommendations": recommendations,
            "collaboration_summary": self._get_collaboration_summary()
        }
    
    def _analyze_intent(self, user_input: str) -> Dict[str, Any]:
        """Analyze user intent to determine which agents to involve."""
        user_lower = user_input.lower()
        
        intent = {
            "primary_agent": None,
            "needs_forecasting": False,
            "needs_supplier_recommendations": False,
            "needs_logistics_optimization": False,
            "needs_inventory_integration": False,
            "complex_request": False
        }
        
        # Inventory-related keywords
        inventory_keywords = ["inventory", "stock", "reorder", "low stock", "out of stock"]
        if any(keyword in user_lower for keyword in inventory_keywords):
            intent["primary_agent"] = "inventory_agent"
            intent["needs_forecasting"] = "forecast" in user_lower or "predict" in user_lower
            intent["needs_supplier_recommendations"] = "supplier" in user_lower or "recommend" in user_lower
        
        # Forecasting-related keywords
        forecasting_keywords = ["forecast", "predict", "demand", "trend", "seasonal"]
        elif any(keyword in user_lower for keyword in forecasting_keywords):
            intent["primary_agent"] = "forecasting_agent"
            intent["needs_inventory_integration"] = "inventory" in user_lower or "stock" in user_lower
        
        # Supplier-related keywords
        supplier_keywords = ["supplier", "vendor", "procurement", "cost", "performance"]
        elif any(keyword in user_lower for keyword in supplier_keywords):
            intent["primary_agent"] = "supplier_agent"
            intent["needs_logistics_optimization"] = "shipping" in user_lower or "logistics" in user_lower
        
        # Complex requests
        complex_keywords = ["optimize", "analyze", "comprehensive", "supply chain", "strategy"]
        if any(keyword in user_lower for keyword in complex_keywords):
            intent["complex_request"] = True
            intent["primary_agent"] = "orchestrator"
        
        return intent
    
    async def _get_forecast_data(self, inventory_data: List[Dict]) -> Dict[str, Any]:
        """Get forecast data from forecasting agent."""
        forecasting_agent = self.agents["forecasting_agent"]
        
        # Convert inventory data to historical demand format
        historical_data = []
        for item in inventory_data:
            historical_data.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "historical_demand": item.get("historical_demand", [])
            })
        
        return forecasting_agent.forecast_demand(historical_data)
    
    def _generate_comprehensive_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate comprehensive recommendations from multi-agent analysis."""
        recommendations = []
        
        # Inventory recommendations
        if "inventory" in results:
            inventory = results["inventory"]
            if inventory.get("low_stock_items"):
                recommendations.append(f"🚨 {len(inventory['low_stock_items'])} items are low on stock and need immediate attention")
            
            if inventory.get("out_of_stock_items"):
                recommendations.append(f"❌ {len(inventory['out_of_stock_items'])} items are out of stock - urgent reordering required")
        
        # Forecast recommendations
        if "forecast" in results:
            recommendations.append("📈 Demand forecasts have been generated - use these for planning reorder points")
        
        # Supplier recommendations
        if "supplier_recommendations" in results:
            recommendations.append("🏭 Supplier recommendations generated for low stock items")
        
        return recommendations
    
    def _get_collaboration_summary(self) -> Dict[str, Any]:
        """Get summary of agent collaborations."""
        return {
            "agents_involved": list(self.agents.keys()),
            "messages_queued": len(self.message_queue),
            "collaboration_active": len(self.message_queue) > 0
        }
    
    def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all agents."""
        return {
            agent_id: agent.capabilities 
            for agent_id, agent in self.agents.items()
        }
