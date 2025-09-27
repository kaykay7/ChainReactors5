"""
🎯 RULE-BASED AGENT ORCHESTRATOR
Main orchestrator that uses rules to route tasks to registered agents based on their capabilities.
"""

from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import json
import asyncio
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentCapability:
    """Defines what an agent can do."""
    name: str
    description: str
    input_types: List[str]
    output_types: List[str]
    keywords: List[str]
    priority: int = 1  # Higher number = higher priority

@dataclass
class AgentRegistration:
    """Registration information for an agent."""
    agent_id: str
    agent_name: str
    capabilities: List[AgentCapability]
    handler: Callable
    status: str = "active"  # active, inactive, busy
    last_used: Optional[datetime] = None
    success_rate: float = 1.0
    response_time: float = 0.0

@dataclass
class TaskRequest:
    """A task request to be routed to appropriate agents."""
    task_id: str
    user_input: str
    context: Dict[str, Any]
    priority: int = 1
    required_capabilities: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

class BaseAgent(ABC):
    """Base class for all agents that can register with the orchestrator."""
    
    def __init__(self, agent_id: str, agent_name: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.capabilities = []
        self.status = "active"
        self.last_used = None
        self.success_rate = 1.0
        self.response_time = 0.0
    
    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """Return the capabilities this agent provides."""
        pass
    
    @abstractmethod
    async def handle_task(self, task: TaskRequest) -> Dict[str, Any]:
        """Handle a task request."""
        pass
    
    def register_with_orchestrator(self, orchestrator: 'RuleBasedOrchestrator'):
        """Register this agent with the orchestrator."""
        orchestrator.register_agent(self)

class RuleBasedOrchestrator:
    """Rule-based orchestrator that routes tasks to registered agents."""
    
    def __init__(self):
        self.registered_agents: Dict[str, AgentRegistration] = {}
        self.routing_rules: List[Dict[str, Any]] = []
        self.task_history: List[TaskRequest] = []
        self.active_tasks: Dict[str, TaskRequest] = {}
        
        # Initialize default routing rules
        self._initialize_default_rules()
    
    def _initialize_default_rules(self):
        """Initialize default routing rules."""
        self.routing_rules = [
            {
                "condition": "inventory" in "user_input.lower()",
                "required_capabilities": ["inventory_management"],
                "priority": 1
            },
            {
                "condition": "forecast" in "user_input.lower() or predict" in "user_input.lower()",
                "required_capabilities": ["demand_forecasting"],
                "priority": 1
            },
            {
                "condition": "supplier" in "user_input.lower()",
                "required_capabilities": ["supplier_management"],
                "priority": 1
            },
            {
                "condition": "order" in "user_input.lower()",
                "required_capabilities": ["order_management"],
                "priority": 1
            },
            {
                "condition": "cost" in "user_input.lower() or optimize" in "user_input.lower()",
                "required_capabilities": ["cost_optimization"],
                "priority": 2
            }
        ]
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator."""
        capabilities = agent.get_capabilities()
        
        registration = AgentRegistration(
            agent_id=agent.agent_id,
            agent_name=agent.agent_name,
            capabilities=capabilities,
            handler=agent.handle_task,
            status="active"
        )
        
        self.registered_agents[agent.agent_id] = registration
        logger.info(f"✅ Registered agent: {agent.agent_name} with {len(capabilities)} capabilities")
        
        # Log capabilities
        for capability in capabilities:
            logger.info(f"   📋 {capability.name}: {capability.description}")
    
    def add_routing_rule(self, rule: Dict[str, Any]):
        """Add a custom routing rule."""
        self.routing_rules.append(rule)
        logger.info(f"📝 Added routing rule: {rule}")
    
    def find_best_agents(self, task: TaskRequest) -> List[AgentRegistration]:
        """Find the best agents for a task based on rules and capabilities."""
        suitable_agents = []
        
        # Apply routing rules
        for rule in self.routing_rules:
            if self._evaluate_rule(rule, task):
                required_caps = rule.get("required_capabilities", [])
                matching_agents = self._find_agents_by_capabilities(required_caps)
                suitable_agents.extend(matching_agents)
        
        # Remove duplicates and sort by priority
        unique_agents = list({agent.agent_id: agent for agent in suitable_agents}.values())
        unique_agents.sort(key=lambda x: (x.success_rate, -x.response_time), reverse=True)
        
        return unique_agents
    
    def _evaluate_rule(self, rule: Dict[str, Any], task: TaskRequest) -> bool:
        """Evaluate if a routing rule matches a task."""
        try:
            # Simple keyword-based evaluation
            user_input_lower = task.user_input.lower()
            condition = rule.get("condition", "")
            
            if "in" in condition and "user_input.lower()" in condition:
                keyword = condition.split('"')[1]
                return keyword in user_input_lower
            
            return False
        except Exception as e:
            logger.error(f"Error evaluating rule: {e}")
            return False
    
    def _find_agents_by_capabilities(self, required_capabilities: List[str]) -> List[AgentRegistration]:
        """Find agents that have the required capabilities."""
        matching_agents = []
        
        for agent in self.registered_agents.values():
            if agent.status != "active":
                continue
                
            agent_capabilities = [cap.name for cap in agent.capabilities]
            
            # Check if agent has any of the required capabilities
            if any(cap in agent_capabilities for cap in required_capabilities):
                matching_agents.append(agent)
        
        return matching_agents
    
    async def route_task(self, task: TaskRequest) -> Dict[str, Any]:
        """Route a task to the best available agent."""
        logger.info(f"🎯 Routing task: {task.task_id}")
        
        # Find suitable agents
        suitable_agents = self.find_best_agents(task)
        
        if not suitable_agents:
            return {
                "success": False,
                "error": "No suitable agents found for this task",
                "task_id": task.task_id
            }
        
        # Try agents in order of suitability
        for agent in suitable_agents:
            try:
                logger.info(f"🤖 Assigning task to: {agent.agent_name}")
                
                # Update agent status
                agent.status = "busy"
                agent.last_used = datetime.now()
                
                # Execute task
                start_time = datetime.now()
                result = await agent.handler(task)
                end_time = datetime.now()
                
                # Update agent metrics
                agent.response_time = (end_time - start_time).total_seconds()
                agent.status = "active"
                agent.success_rate = min(1.0, agent.success_rate + 0.1)
                
                # Store task history
                self.task_history.append(task)
                
                logger.info(f"✅ Task completed by {agent.agent_name} in {agent.response_time:.2f}s")
                
                return {
                    "success": True,
                    "result": result,
                    "agent_used": agent.agent_name,
                    "response_time": agent.response_time,
                    "task_id": task.task_id
                }
                
            except Exception as e:
                logger.error(f"❌ Agent {agent.agent_name} failed: {e}")
                agent.status = "active"
                agent.success_rate = max(0.0, agent.success_rate - 0.1)
                continue
        
        return {
            "success": False,
            "error": "All suitable agents failed to process the task",
            "task_id": task.task_id
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all registered agents."""
        return {
            "total_agents": len(self.registered_agents),
            "active_agents": len([a for a in self.registered_agents.values() if a.status == "active"]),
            "busy_agents": len([a for a in self.registered_agents.values() if a.status == "busy"]),
            "agents": {
                agent_id: {
                    "name": agent.agent_name,
                    "status": agent.status,
                    "capabilities": [cap.name for cap in agent.capabilities],
                    "success_rate": agent.success_rate,
                    "response_time": agent.response_time,
                    "last_used": agent.last_used.isoformat() if agent.last_used else None
                }
                for agent_id, agent in self.registered_agents.items()
            }
        }
    
    def get_routing_rules(self) -> List[Dict[str, Any]]:
        """Get all routing rules."""
        return self.routing_rules

# Global orchestrator instance
rule_based_orchestrator = RuleBasedOrchestrator()

# Example agent implementations
class InventoryManagementAgent(BaseAgent):
    """Agent specialized in inventory management."""
    
    def __init__(self):
        super().__init__("inventory_agent", "Inventory Management Agent")
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="inventory_management",
                description="Manage inventory levels, reorder points, and stock optimization",
                input_types=["inventory_data", "stock_levels"],
                output_types=["inventory_recommendations", "reorder_alerts"],
                keywords=["inventory", "stock", "reorder", "warehouse"]
            ),
            AgentCapability(
                name="stock_analysis",
                description="Analyze stock levels and identify optimization opportunities",
                input_types=["inventory_data"],
                output_types=["analysis_report"],
                keywords=["analyze", "stock", "levels", "optimization"]
            )
        ]
    
    async def handle_task(self, task: TaskRequest) -> Dict[str, Any]:
        """Handle inventory-related tasks."""
        logger.info(f"📦 Inventory agent handling: {task.user_input}")
        
        # Simulate inventory processing
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "agent": "inventory_agent",
            "action": "inventory_analysis",
            "result": "Inventory levels analyzed. 3 items need reordering.",
            "recommendations": [
                "Reorder microprocessors (current: 5, min: 10)",
                "Reorder memory chips (current: 8, min: 15)",
                "Reorder steel brackets (current: 2, min: 20)"
            ]
        }

class DemandForecastingAgent(BaseAgent):
    """Agent specialized in demand forecasting."""
    
    def __init__(self):
        super().__init__("forecasting_agent", "Demand Forecasting Agent")
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="demand_forecasting",
                description="Predict future demand based on historical data and trends",
                input_types=["historical_data", "market_trends"],
                output_types=["demand_forecast", "trend_analysis"],
                keywords=["forecast", "predict", "demand", "trends"]
            ),
            AgentCapability(
                name="market_analysis",
                description="Analyze market conditions and external factors",
                input_types=["market_data"],
                output_types=["market_insights"],
                keywords=["market", "analysis", "trends", "external"]
            )
        ]
    
    async def handle_task(self, task: TaskRequest) -> Dict[str, Any]:
        """Handle forecasting-related tasks."""
        logger.info(f"📈 Forecasting agent handling: {task.user_input}")
        
        # Simulate forecasting processing
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "agent": "forecasting_agent",
            "action": "demand_forecast",
            "result": "Demand forecast generated for next 3 months",
            "forecast": {
                "microprocessors": {"q1": 150, "q2": 180, "q3": 200},
                "memory_chips": {"q1": 200, "q2": 220, "q3": 250},
                "steel_brackets": {"q1": 100, "q2": 120, "q3": 140}
            }
        }

class SupplierManagementAgent(BaseAgent):
    """Agent specialized in supplier management."""
    
    def __init__(self):
        super().__init__("supplier_agent", "Supplier Management Agent")
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="supplier_management",
                description="Manage supplier relationships and performance evaluation",
                input_types=["supplier_data", "performance_metrics"],
                output_types=["supplier_recommendations", "performance_report"],
                keywords=["supplier", "vendor", "performance", "relationship"]
            ),
            AgentCapability(
                name="supplier_evaluation",
                description="Evaluate supplier performance and identify issues",
                input_types=["supplier_data"],
                output_types=["evaluation_report"],
                keywords=["evaluate", "performance", "supplier", "assessment"]
            )
        ]
    
    async def handle_task(self, task: TaskRequest) -> Dict[str, Any]:
        """Handle supplier-related tasks."""
        logger.info(f"🏭 Supplier agent handling: {task.user_input}")
        
        # Simulate supplier processing
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "agent": "supplier_agent",
            "action": "supplier_analysis",
            "result": "Supplier performance analyzed",
            "top_suppliers": [
                {"name": "TechCorp Solutions", "score": 95, "delivery_time": "2 days"},
                {"name": "Global Parts Inc", "score": 88, "delivery_time": "3 days"},
                {"name": "Premium Components", "score": 92, "delivery_time": "1 day"}
            ]
        }

# Initialize and register agents
def initialize_rule_based_system():
    """Initialize the rule-based agent system."""
    logger.info("🚀 Initializing Rule-Based Agent System")
    
    # Create agents
    inventory_agent = InventoryManagementAgent()
    forecasting_agent = DemandForecastingAgent()
    supplier_agent = SupplierManagementAgent()
    
    # Register agents
    inventory_agent.register_with_orchestrator(rule_based_orchestrator)
    forecasting_agent.register_with_orchestrator(rule_based_orchestrator)
    supplier_agent.register_with_orchestrator(rule_based_orchestrator)
    
    logger.info(f"✅ System initialized with {len(rule_based_orchestrator.registered_agents)} agents")
    
    return rule_based_orchestrator

# Initialize the system
orchestrator = initialize_rule_based_system()
