# 🤖 LLM Context Explanation

## 🎯 **What Context is Sent to the LLM**

The LLM receives rich contextual information from the memory system to make intelligent decisions and provide relevant responses.

## 📊 **Context Types Sent to LLM**

### **1. 🗣️ Conversation Context**
```python
# Recent chat history sent to LLM
{
    "recent_conversations": [
        "User: Analyze our inventory levels",
        "Agent: Found 3 low stock items that need attention",
        "User: Which suppliers should we use?",
        "Agent: I recommend TechCorp Solutions based on your preferences"
    ],
    "agent_type": "inventory_agent"
}
```

### **2. 🔍 Semantic Search Results**
```python
# Relevant memories retrieved by semantic search
{
    "memories": [
        {
            "text": "Agent: inventory_agent\nType: stock_analysis\nTimestamp: 2024-01-20T10:30:00Z\nUser Input: Check our stock levels\nResponse: Found 3 low stock items: Product A, B, C\nData: {\"low_stock_items\": [\"Product A\", \"Product B\", \"Product C\"]}",
            "metadata": {
                "agent_id": "inventory_agent",
                "interaction_type": "stock_analysis",
                "timestamp": "2024-01-20T10:30:00Z"
            },
            "score": 0.95
        }
    ]
}
```

### **3. 🤝 Collaboration Context**
```python
# Agent collaboration history
{
    "collaboration_history": [
        {
            "sender": "inventory_agent",
            "recipient": "supplier_agent",
            "message_type": "supplier_recommendations_request",
            "timestamp": "2024-01-20T10:30:00Z",
            "data": {"low_stock_items": ["Product A"]}
        }
    ],
    "agent_type": "inventory_agent"
}
```

### **4. 🧠 Learning Context**
```python
# Learning insights and adaptations
{
    "learning_insights": [
        {
            "text": "Learning Insight: Product A consistently shows seasonal demand patterns in Q4\nContext: {\"product\": \"Product A\", \"pattern\": \"seasonal\", \"quarter\": \"Q4\"}",
            "metadata": {
                "agent_id": "inventory_agent",
                "insight": "Product A consistently shows seasonal demand patterns in Q4",
                "context": {"product": "Product A", "pattern": "seasonal", "quarter": "Q4"},
                "timestamp": "2024-01-20T10:30:00Z"
            },
            "score": 0.88
        }
    ]
}
```

### **5. 👤 User Context**
```python
# User preferences and behavior patterns
{
    "user_preferences": {
        "user_id": "user_123",
        "preferences": {
            "preferred_suppliers": ["TechCorp Solutions"],
            "risk_tolerance": "low",
            "optimization_priority": "cost"
        }
    }
}
```

## 🔄 **How Context is Formatted for LLM**

### **1. 📝 Interaction Formatting**
```python
def _format_interaction_for_memory(self, interaction: Dict[str, Any]) -> str:
    """Format interaction data for storage in memory."""
    formatted_text = f"""
Agent: {interaction['agent_id']}
Type: {interaction['interaction_type']}
Timestamp: {interaction['timestamp']}
"""
    
    if interaction.get('user_input'):
        formatted_text += f"User Input: {interaction['user_input']}\n"
    
    if interaction.get('response'):
        formatted_text += f"Response: {interaction['response']}\n"
    
    if interaction.get('data'):
        formatted_text += f"Data: {json.dumps(interaction['data'], indent=2)}\n"
    
    return formatted_text
```

### **2. 🔍 Memory Retrieval Context**
```python
def retrieve_agent_memory(self, agent_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Retrieve relevant memories for an agent using semantic search."""
    
    # Perform semantic search
    query_engine = agent_memory["index"].as_query_engine(similarity_top_k=limit)
    response = query_engine.query(query)
    
    # Extract relevant memories with context
    memories = []
    for node in response.source_nodes:
        memories.append({
            "text": node.text,           # Full formatted text
            "metadata": node.metadata,   # Structured metadata
            "score": node.score          # Relevance score
        })
    
    return memories
```

### **3. 📊 Analysis Results Context**
```python
# Analysis results formatted for LLM
doc_text = f"Analysis Results ({analysis_type}): {json.dumps(results, indent=2)}"
if recommendations:
    doc_text += f"\nRecommendations: {', '.join(recommendations)}"

# Example formatted text sent to LLM:
"""
Analysis Results (inventory_analysis): {
  "low_stock_items": ["Product A", "Product B"],
  "out_of_stock_items": ["Product C"],
  "recommendations": ["Reorder Product A", "Monitor Product B"]
}
Recommendations: Reorder Product A immediately, Monitor Product B closely
"""
```

## 🎯 **Context Assembly Process**

### **1. 🔍 Query Processing**
```python
# User query: "Analyze our inventory levels"
# LLM receives context:

# Step 1: Get recent conversations
recent_context = memory_manager.get_agent_context("inventory_agent", "recent")

# Step 2: Get relevant memories
relevant_memories = memory_manager.retrieve_agent_memory(
    "inventory_agent", "inventory analysis stock levels", limit=5
)

# Step 3: Get collaboration history
collaboration_context = memory_manager.get_agent_context("inventory_agent", "collaboration")

# Step 4: Get learning insights
learning_context = memory_manager.get_agent_learning_history("inventory_agent")
```

### **2. 📊 Context Combination**
```python
# Combined context sent to LLM
llm_context = {
    "user_query": "Analyze our inventory levels",
    "recent_conversations": recent_context["recent_conversations"],
    "relevant_memories": relevant_memories,
    "collaboration_history": collaboration_context["collaboration_history"],
    "learning_insights": learning_context,
    "user_preferences": user_preferences,
    "agent_type": "inventory_agent"
}
```

## 🧠 **LLM Context Structure**

### **1. 📋 Complete Context Example**
```python
{
    "user_query": "Analyze our inventory levels",
    "agent_type": "inventory_agent",
    "recent_conversations": [
        "User: Check our stock levels",
        "Agent: Found 3 low stock items: Product A, B, C"
    ],
    "relevant_memories": [
        {
            "text": "Agent: inventory_agent\nType: stock_analysis\nUser Input: Check stock levels\nResponse: Found 3 low stock items\nData: {\"low_stock_items\": [\"Product A\", \"Product B\", \"Product C\"]}",
            "metadata": {
                "agent_id": "inventory_agent",
                "interaction_type": "stock_analysis",
                "timestamp": "2024-01-20T10:30:00Z"
            },
            "score": 0.95
        }
    ],
    "collaboration_history": [
        {
            "sender": "inventory_agent",
            "recipient": "supplier_agent",
            "message_type": "supplier_recommendations_request",
            "data": {"low_stock_items": ["Product A"]}
        }
    ],
    "learning_insights": [
        {
            "text": "Learning Insight: Product A shows seasonal patterns in Q4",
            "context": {"product": "Product A", "pattern": "seasonal", "quarter": "Q4"}
        }
    ],
    "user_preferences": {
        "preferred_suppliers": ["TechCorp Solutions"],
        "risk_tolerance": "low"
    }
}
```

### **2. 🎯 Context Prioritization**
```python
# Context is prioritized by relevance score
# Higher scores = more relevant to current query
# LLM receives top 5 most relevant memories
# Recent conversations provide immediate context
# Learning insights provide long-term patterns
```

## 🔄 **Context Flow to LLM**

### **1. 📥 Input Processing**
```
User Query → Memory Retrieval → Context Assembly → LLM Processing → Response
```

### **2. 🔍 Memory Retrieval Steps**
```
1. Semantic search for relevant memories
2. Retrieve recent conversation history
3. Get collaboration history
4. Fetch learning insights
5. Load user preferences
6. Combine into structured context
```

### **3. 📊 Context Formatting**
```
1. Format interaction data for readability
2. Include metadata for context
3. Add relevance scores for prioritization
4. Structure for LLM consumption
5. Include timestamps for temporal context
```

## 🎯 **LLM Context Benefits**

### **✅ Rich Contextual Information**
- **Historical data** from past interactions
- **Learning patterns** from previous analyses
- **User preferences** for personalization
- **Collaboration history** for coordination

### **✅ Intelligent Memory Retrieval**
- **Semantic search** finds relevant memories
- **Relevance scoring** prioritizes important context
- **Context-aware** memory selection
- **Temporal awareness** from timestamps

### **✅ Personalized Responses**
- **User preferences** influence recommendations
- **Learning insights** improve accuracy
- **Collaboration patterns** optimize workflows
- **Historical context** provides continuity

### **✅ Adaptive Learning**
- **Pattern recognition** from past interactions
- **Trend analysis** from historical data
- **Seasonal awareness** from learning insights
- **Performance optimization** from collaboration history

## 🚀 **Context in Action**

### **Example 1: Inventory Analysis**
```python
# User: "Analyze our inventory levels"
# LLM receives:
{
    "user_query": "Analyze our inventory levels",
    "recent_conversations": ["User: Check stock levels", "Agent: Found 3 low stock items"],
    "relevant_memories": [past inventory analyses],
    "learning_insights": ["Product A shows seasonal patterns"],
    "user_preferences": {"risk_tolerance": "low"}
}

# LLM uses this context to provide personalized, informed analysis
```

### **Example 2: Supplier Recommendations**
```python
# User: "Which suppliers should we use?"
# LLM receives:
{
    "user_query": "Which suppliers should we use?",
    "collaboration_history": [inventory-supplier collaborations],
    "learning_insights": ["TechCorp Solutions consistently delivers"],
    "user_preferences": {"preferred_suppliers": ["TechCorp Solutions"]}
}

# LLM uses this context to provide personalized supplier recommendations
```

## 🎉 **Summary**

**The LLM receives rich contextual information including:**

1. **🗣️ Conversation History** - Recent user-agent interactions
2. **🔍 Relevant Memories** - Semantically similar past experiences
3. **🤝 Collaboration History** - Agent-to-agent communications
4. **🧠 Learning Insights** - Patterns and adaptations learned over time
5. **👤 User Preferences** - Personalization data for tailored responses
6. **📊 Analysis Results** - Past analysis outcomes and recommendations
7. **⏰ Temporal Context** - Timestamps for time-aware responses

This creates **intelligent, context-aware agents** that provide personalized, informed responses based on rich historical and learning context! 🚀
