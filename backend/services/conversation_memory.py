"""
Conversation Memory Service
Manages conversation context and history
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class ConversationMemory:
    """
    Manages conversation context across sessions
    """
    
    def __init__(self):
        # In-memory storage (in production, use Redis or database)
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        self.user_preferences: Dict[int, Dict[str, Any]] = {}
        self.session_context: Dict[str, Dict[str, Any]] = {}
    
    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add a message to conversation history
        """
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.conversations[session_id].append(message)
        
        # Keep only last 20 messages for efficiency
        if len(self.conversations[session_id]) > 20:
            self.conversations[session_id] = self.conversations[session_id][-20:]
        
        logger.info(f"Added message to session {session_id}")
    
    def get_conversation_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent conversation history
        """
        if session_id not in self.conversations:
            return []
        
        return self.conversations[session_id][-limit:]
    
    def get_context_for_llm(
        self,
        session_id: str,
        max_messages: int = 5
    ) -> str:
        """
        Format conversation history for LLM context
        """
        history = self.get_conversation_history(session_id, limit=max_messages)
        
        if not history:
            return "No previous conversation"
        
        formatted = "Previous conversation:\n"
        for msg in history:
            formatted += f"{msg['role'].capitalize()}: {msg['content'][:200]}...\n"
        
        return formatted
    
    def update_session_context(
        self,
        session_id: str,
        key: str,
        value: Any
    ):
        """
        Update context variables for a session
        """
        if session_id not in self.session_context:
            self.session_context[session_id] = {}
        
        self.session_context[session_id][key] = value
        logger.info(f"Updated context for session {session_id}: {key}")
    
    def get_session_context(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Get all context for a session
        """
        return self.session_context.get(session_id, {})
    
    def update_user_preferences(
        self,
        user_id: int,
        preferences: Dict[str, Any]
    ):
        """
        Update user preferences (favorite domains, common queries, etc.)
        """
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        self.user_preferences[user_id].update(preferences)
        logger.info(f"Updated preferences for user {user_id}")
    
    def get_user_preferences(
        self,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Get user preferences
        """
        return self.user_preferences.get(user_id, {})
    
    def track_domain_usage(
        self,
        user_id: int,
        domain: str
    ):
        """
        Track which domains user queries most
        """
        prefs = self.get_user_preferences(user_id)
        
        if "domain_usage" not in prefs:
            prefs["domain_usage"] = {}
        
        if domain not in prefs["domain_usage"]:
            prefs["domain_usage"][domain] = 0
        
        prefs["domain_usage"][domain] += 1
        
        self.update_user_preferences(user_id, prefs)
    
    def get_favorite_domain(
        self,
        user_id: int
    ) -> Optional[str]:
        """
        Get user's most-used domain
        """
        prefs = self.get_user_preferences(user_id)
        domain_usage = prefs.get("domain_usage", {})
        
        if not domain_usage:
            return None
        
        return max(domain_usage.items(), key=lambda x: x[1])[0]
    
    def clear_session(
        self,
        session_id: str
    ):
        """
        Clear conversation history for a session
        """
        if session_id in self.conversations:
            del self.conversations[session_id]
        
        if session_id in self.session_context:
            del self.session_context[session_id]
        
        logger.info(f"Cleared session {session_id}")
    
    def get_conversation_summary(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Get summary statistics for a conversation
        """
        history = self.get_conversation_history(session_id, limit=100)
        
        user_messages = [m for m in history if m["role"] == "user"]
        assistant_messages = [m for m in history if m["role"] == "assistant"]
        
        # Extract domains mentioned
        domains_mentioned = set()
        for msg in history:
            metadata = msg.get("metadata", {})
            if "domain" in metadata:
                domains_mentioned.add(metadata["domain"])
        
        return {
            "total_messages": len(history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "domains_mentioned": list(domains_mentioned),
            "session_started": history[0]["timestamp"] if history else None,
            "last_activity": history[-1]["timestamp"] if history else None
        }


# Global instance
_memory = ConversationMemory()


def get_conversation_memory() -> ConversationMemory:
    """Get global conversation memory instance"""
    return _memory
