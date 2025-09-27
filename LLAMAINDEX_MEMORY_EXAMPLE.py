"""
🧠 LlamaIndex Memory Persistence Example
Demonstrates how to use LlamaIndex for persistent agent memory.
"""

import asyncio
from datetime import datetime
from agent.agent.memory_manager import AgentMemoryManager
from agent.agent.agent_orchestrator import AgentOrchestrator

async def demonstrate_memory_persistence():
    """Demonstrate LlamaIndex memory persistence capabilities."""
    
    print("🧠 LlamaIndex Memory Persistence Demo")
    print("=" * 50)
    
    # Initialize orchestrator with memory
    orchestrator = AgentOrchestrator(memory_dir="./demo_memory")
    
    # Simulate user interactions
    user_requests = [
        "Analyze our inventory levels and identify low stock items",
        "What are the demand forecasts for next quarter?",
        "Which suppliers should we use for Product A?",
        "Optimize our supply chain for the next quarter"
    ]
    
    print("\n📝 Storing User Interactions...")
    for i, request in enumerate(user_requests, 1):
        print(f"\n{i}. User Request: {request}")
        
        # Process request (this stores in memory)
        context = {
            "inventory_data": [
                {"id": "PROD-001", "name": "Product A", "current_stock": 150, "min_stock": 50},
                {"id": "PROD-002", "name": "Product B", "current_stock": 25, "min_stock": 30}
            ],
            "supplier_data": [
                {"id": "SUP-001", "name": "TechCorp Solutions", "reliability_score": 95},
                {"id": "SUP-002", "name": "Global Parts Inc", "reliability_score": 78}
            ]
        }
        
        # This automatically stores the interaction in memory
        result = await orchestrator.process_user_request(request, context)
        print(f"   Response Type: {result.get('response_type', 'unknown')}")
    
    print("\n🔍 Retrieving Memory Insights...")
    
    # Get memory statistics
    memory_stats = orchestrator.memory_manager.get_memory_stats()
    print(f"\nMemory Statistics:")
    print(f"- Total Agents: {memory_stats['total_agents']}")
    print(f"- Collaboration Events: {memory_stats['collaboration_events']}")
    
    # Demonstrate memory retrieval
    print("\n📚 Retrieving Agent Memories...")
    
    # Get inventory agent's recent context
    inventory_context = orchestrator.memory_manager.get_agent_context("inventory_agent", "recent")
    print(f"Inventory Agent Recent Context: {len(inventory_context.get('recent_conversations', []))} conversations")
    
    # Get collaboration history
    collaboration_context = orchestrator.memory_manager.get_agent_context("orchestrator", "collaboration")
    print(f"Collaboration Events: {len(collaboration_context.get('collaboration_history', []))} events")
    
    # Demonstrate semantic search
    print("\n🔍 Semantic Memory Search...")
    
    # Search for inventory-related memories
    inventory_memories = orchestrator.memory_manager.retrieve_agent_memory(
        "inventory_agent", "stock levels analysis recommendations", limit=3
    )
    print(f"Found {len(inventory_memories)} inventory-related memories")
    
    for memory in inventory_memories:
        print(f"  - {memory['metadata'].get('interaction_type', 'unknown')}: {memory['text'][:100]}...")
    
    # Demonstrate learning insights
    print("\n🧠 Learning Insights...")
    
    # Store a learning insight
    orchestrator.memory_manager.store_learning_insights(
        "inventory_agent", 
        "Product A consistently shows seasonal demand patterns in Q4",
        {"product": "Product A", "pattern": "seasonal", "quarter": "Q4"}
    )
    
    # Retrieve learning history
    learning_history = orchestrator.memory_manager.get_agent_learning_history("inventory_agent")
    print(f"Inventory Agent Learning History: {len(learning_history)} insights")
    
    # Demonstrate user preferences
    print("\n👤 User Preferences...")
    
    # Store user preferences
    orchestrator.memory_manager.store_user_preferences("user_123", {
        "preferred_suppliers": ["TechCorp Solutions"],
        "risk_tolerance": "low",
        "optimization_priority": "cost"
    })
    
    # Retrieve user preferences
    preferences = orchestrator.memory_manager.get_user_preferences("user_123")
    print(f"User Preferences: {preferences}")
    
    # Demonstrate analysis result storage
    print("\n📊 Storing Analysis Results...")
    
    # Store analysis results
    analysis_results = {
        "low_stock_items": ["Product B"],
        "recommended_actions": ["Reorder Product B from TechCorp Solutions"],
        "confidence_score": 0.95
    }
    
    orchestrator.memory_manager.store_analysis_results(
        "inventory_agent", "stock_analysis", analysis_results, 
        ["Monitor Product B closely", "Consider safety stock increase"]
    )
    
    print("Analysis results stored successfully!")
    
    # Demonstrate memory export
    print("\n📤 Memory Export...")
    
    export_path = "./inventory_agent_memory_export.json"
    export_result = orchestrator.memory_manager.export_memory("inventory_agent", export_path)
    print(f"Export Result: {export_result}")
    
    print("\n🎉 Memory Persistence Demo Complete!")
    print("\nKey Benefits:")
    print("✅ Persistent memory across sessions")
    print("✅ Semantic search capabilities")
    print("✅ Agent collaboration history")
    print("✅ Learning insights storage")
    print("✅ User preference personalization")
    print("✅ Analysis result tracking")

def demonstrate_memory_benefits():
    """Show the benefits of persistent memory."""
    
    print("\n🚀 Benefits of LlamaIndex Memory Persistence")
    print("=" * 50)
    
    benefits = {
        "🧠 Learning & Adaptation": [
            "Agents learn from past interactions",
            "Improve recommendations over time",
            "Adapt to user preferences",
            "Remember successful strategies"
        ],
        "🔍 Context Awareness": [
            "Access to historical data",
            "Pattern recognition across sessions",
            "Trend analysis capabilities",
            "Seasonal pattern detection"
        ],
        "🤝 Agent Collaboration": [
            "Track agent-to-agent communications",
            "Learn from collaboration patterns",
            "Optimize workflow coordination",
            "Share insights between agents"
        ],
        "👤 Personalization": [
            "Remember user preferences",
            "Customize recommendations",
            "Adapt to user behavior",
            "Provide personalized insights"
        ],
        "📊 Performance Tracking": [
            "Monitor agent performance",
            "Track recommendation accuracy",
            "Identify improvement areas",
            "Measure collaboration effectiveness"
        ]
    }
    
    for category, items in benefits.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  ✅ {item}")

if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(demonstrate_memory_persistence())
    demonstrate_memory_benefits()
