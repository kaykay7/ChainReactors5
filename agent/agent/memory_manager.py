"""
🧠 MEMORY MANAGER
LlamaIndex-based persistent memory for specialized agents.
"""

from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core import (
    VectorStoreIndex, 
    Document, 
    ServiceContext,
    Settings
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

class AgentMemoryManager:
    """Manages persistent memory for specialized agents using LlamaIndex."""
    
    def __init__(self, memory_dir: str = "./agent_memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        # Initialize LlamaIndex components
        self._setup_llamaindex()
        
        # Agent-specific memory stores
        self.agent_memories = {
            "inventory_agent": self._create_agent_memory("inventory"),
            "forecasting_agent": self._create_agent_memory("forecasting"),
            "supplier_agent": self._create_agent_memory("supplier"),
            "orchestrator": self._create_agent_memory("orchestrator")
        }
        
        # Conversation memory
        self.conversation_memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
        
        # Agent collaboration history
        self.collaboration_history = []
    
    def _setup_llamaindex(self):
        """Setup LlamaIndex components for memory persistence."""
        # Configure LlamaIndex settings
        Settings.llm = OpenAI(model="gpt-4", temperature=0.1)
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
        
        # Create storage context for persistence
        self.storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore(),
            index_store=SimpleIndexStore(),
            vector_store=SimpleVectorStore()
        )
    
    def _create_agent_memory(self, agent_type: str) -> Dict[str, Any]:
        """Create memory store for a specific agent."""
        agent_memory_dir = self.memory_dir / agent_type
        agent_memory_dir.mkdir(exist_ok=True)
        
        # Create agent-specific storage
        storage_context = StorageContext.from_defaults(
            docstore=SimpleDocumentStore.from_persist_dir(str(agent_memory_dir)),
            index_store=SimpleIndexStore.from_persist_dir(str(agent_memory_dir)),
            vector_store=SimpleVectorStore.from_persist_dir(str(agent_memory_dir))
        )
        
        # Create vector index for semantic search
        index = VectorStoreIndex.from_vector_store(
            storage_context.vector_store,
            storage_context=storage_context
        )
        
        return {
            "index": index,
            "storage_context": storage_context,
            "chat_memory": ChatMemoryBuffer.from_defaults(token_limit=2000),
            "agent_type": agent_type,
            "memory_dir": agent_memory_dir
        }
    
    def store_agent_interaction(self, agent_id: str, interaction_type: str, 
                              data: Dict[str, Any], user_input: str = None, 
                              response: str = None) -> str:
        """Store an agent interaction in persistent memory."""
        agent_memory = self.agent_memories.get(agent_id)
        if not agent_memory:
            raise ValueError(f"Unknown agent: {agent_id}")
        
        # Create interaction document
        interaction_doc = {
            "agent_id": agent_id,
            "interaction_type": interaction_type,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "user_input": user_input,
            "response": response
        }
        
        # Create LlamaIndex document
        doc_text = self._format_interaction_for_memory(interaction_doc)
        document = Document(
            text=doc_text,
            metadata={
                "agent_id": agent_id,
                "interaction_type": interaction_type,
                "timestamp": interaction_doc["timestamp"]
            }
        )
        
        # Add to agent's memory index
        agent_memory["index"].insert(document)
        
        # Add to chat memory
        if user_input and response:
            agent_memory["chat_memory"].put(
                f"User: {user_input}\nAgent: {response}"
            )
        
        # Persist to disk
        agent_memory["storage_context"].persist(persist_dir=str(agent_memory["memory_dir"]))
        
        return f"Stored interaction for {agent_id}"
    
    def store_collaboration_event(self, sender_agent: str, recipient_agent: str, 
                               message_type: str, data: Dict[str, Any]) -> str:
        """Store agent-to-agent collaboration events."""
        collaboration_event = {
            "sender": sender_agent,
            "recipient": recipient_agent,
            "message_type": message_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        # Store in collaboration history
        self.collaboration_history.append(collaboration_event)
        
        # Store in orchestrator memory
        orchestrator_memory = self.agent_memories["orchestrator"]
        doc_text = f"Collaboration: {sender_agent} -> {recipient_agent} ({message_type})"
        document = Document(
            text=doc_text,
            metadata=collaboration_event
        )
        orchestrator_memory["index"].insert(document)
        
        # Persist orchestrator memory
        orchestrator_memory["storage_context"].persist(
            persist_dir=str(orchestrator_memory["memory_dir"])
        )
        
        return f"Stored collaboration: {sender_agent} -> {recipient_agent}"
    
    def retrieve_agent_memory(self, agent_id: str, query: str, 
                             limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant memories for an agent using semantic search."""
        agent_memory = self.agent_memories.get(agent_id)
        if not agent_memory:
            return []
        
        # Perform semantic search
        query_engine = agent_memory["index"].as_query_engine(similarity_top_k=limit)
        response = query_engine.query(query)
        
        # Extract relevant memories
        memories = []
        for node in response.source_nodes:
            memories.append({
                "text": node.text,
                "metadata": node.metadata,
                "score": node.score
            })
        
        return memories
    
    def get_agent_context(self, agent_id: str, context_type: str = "recent") -> Dict[str, Any]:
        """Get contextual information for an agent."""
        agent_memory = self.agent_memories.get(agent_id)
        if not agent_memory:
            return {}
        
        if context_type == "recent":
            # Get recent chat history
            recent_messages = agent_memory["chat_memory"].get_all()
            return {
                "recent_conversations": recent_messages,
                "agent_type": agent_memory["agent_type"]
            }
        
        elif context_type == "collaboration":
            # Get collaboration history
            collaboration_events = [
                event for event in self.collaboration_history 
                if event["sender"] == agent_id or event["recipient"] == agent_id
            ]
            return {
                "collaboration_history": collaboration_events[-10:],  # Last 10 events
                "agent_type": agent_memory["agent_type"]
            }
        
        elif context_type == "performance":
            # Get performance-related memories
            performance_memories = self.retrieve_agent_memory(
                agent_id, "performance analysis results recommendations", limit=10
            )
            return {
                "performance_memories": performance_memories,
                "agent_type": agent_memory["agent_type"]
            }
        
        return {}
    
    def store_analysis_results(self, agent_id: str, analysis_type: str, 
                             results: Dict[str, Any], recommendations: List[str] = None) -> str:
        """Store analysis results for future reference."""
        analysis_doc = {
            "agent_id": agent_id,
            "analysis_type": analysis_type,
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "recommendations": recommendations or []
        }
        
        # Store in agent memory
        doc_text = f"Analysis Results ({analysis_type}): {json.dumps(results, indent=2)}"
        if recommendations:
            doc_text += f"\nRecommendations: {', '.join(recommendations)}"
        
        document = Document(
            text=doc_text,
            metadata={
                "agent_id": agent_id,
                "analysis_type": analysis_type,
                "timestamp": analysis_doc["timestamp"]
            }
        )
        
        agent_memory = self.agent_memories[agent_id]
        agent_memory["index"].insert(document)
        agent_memory["storage_context"].persist(
            persist_dir=str(agent_memory["memory_dir"])
        )
        
        return f"Stored {analysis_type} analysis results for {agent_id}"
    
    def get_historical_insights(self, agent_id: str, insight_type: str) -> List[Dict[str, Any]]:
        """Get historical insights of a specific type."""
        insights = self.retrieve_agent_memory(
            agent_id, f"{insight_type} historical data trends patterns", limit=10
        )
        return insights
    
    def store_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> str:
        """Store user preferences for personalization."""
        preferences_doc = {
            "user_id": user_id,
            "preferences": preferences,
            "timestamp": datetime.now().isoformat()
        }
        
        # Store in orchestrator memory (user preferences are global)
        orchestrator_memory = self.agent_memories["orchestrator"]
        doc_text = f"User Preferences: {json.dumps(preferences, indent=2)}"
        document = Document(
            text=doc_text,
            metadata=preferences_doc
        )
        
        orchestrator_memory["index"].insert(document)
        orchestrator_memory["storage_context"].persist(
            persist_dir=str(orchestrator_memory["memory_dir"])
        )
        
        return f"Stored preferences for user {user_id}"
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Retrieve user preferences."""
        preferences = self.retrieve_agent_memory(
            "orchestrator", f"user preferences {user_id}", limit=1
        )
        
        if preferences:
            # Extract preferences from the most recent match
            return preferences[0].get("metadata", {}).get("preferences", {})
        
        return {}
    
    def store_learning_insights(self, agent_id: str, insight: str, 
                              context: Dict[str, Any]) -> str:
        """Store learning insights that agents can use to improve."""
        learning_doc = {
            "agent_id": agent_id,
            "insight": insight,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        
        agent_memory = self.agent_memories[agent_id]
        doc_text = f"Learning Insight: {insight}\nContext: {json.dumps(context, indent=2)}"
        document = Document(
            text=doc_text,
            metadata=learning_doc
        )
        
        agent_memory["index"].insert(document)
        agent_memory["storage_context"].persist(
            persist_dir=str(agent_memory["memory_dir"])
        )
        
        return f"Stored learning insight for {agent_id}"
    
    def get_agent_learning_history(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get learning history for an agent."""
        return self.retrieve_agent_memory(
            agent_id, "learning insights improvements adaptations", limit=20
        )
    
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
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about memory usage."""
        stats = {
            "total_agents": len(self.agent_memories),
            "collaboration_events": len(self.collaboration_history),
            "agent_memories": {}
        }
        
        for agent_id, memory in self.agent_memories.items():
            # Get approximate memory size
            memory_dir = memory["memory_dir"]
            if memory_dir.exists():
                total_size = sum(f.stat().st_size for f in memory_dir.rglob('*') if f.is_file())
                stats["agent_memories"][agent_id] = {
                    "memory_dir": str(memory_dir),
                    "size_bytes": total_size,
                    "agent_type": memory["agent_type"]
                }
        
        return stats
    
    def clear_agent_memory(self, agent_id: str) -> str:
        """Clear all memory for a specific agent."""
        if agent_id not in self.agent_memories:
            return f"Agent {agent_id} not found"
        
        agent_memory = self.agent_memories[agent_id]
        memory_dir = agent_memory["memory_dir"]
        
        # Clear the memory directory
        if memory_dir.exists():
            import shutil
            shutil.rmtree(memory_dir)
            memory_dir.mkdir(exist_ok=True)
        
        # Recreate the memory store
        self.agent_memories[agent_id] = self._create_agent_memory(agent_memory["agent_type"])
        
        return f"Cleared memory for agent {agent_id}"
    
    def export_memory(self, agent_id: str, export_path: str) -> str:
        """Export agent memory to a file."""
        if agent_id not in self.agent_memories:
            return f"Agent {agent_id} not found"
        
        # Get all memories for the agent
        memories = self.retrieve_agent_memory(agent_id, "", limit=1000)
        
        # Export to JSON
        export_data = {
            "agent_id": agent_id,
            "export_timestamp": datetime.now().isoformat(),
            "memories": memories
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return f"Exported memory for {agent_id} to {export_path}"
