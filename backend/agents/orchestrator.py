"""
AI Agent Orchestrator using LangGraph
Coordinates 5 specialized agents for data analytics
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from anthropic import Anthropic
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from utils.config import settings
from agents.welcoming_agent import WelcomingAgent
from agents.supervisor_agent import SupervisorAgent
from agents.data_manager_agent import DataManagerAgent
from agents.data_engineer_agent import DataEngineerAgent
from agents.analytics_expert_agent import AnalyticsExpertAgent
from services.conversation_memory import get_conversation_memory

logger = logging.getLogger(__name__)


class AgentState(Dict):
    """
    Shared state between agents
    """
    user_message: str
    domain: Optional[str]
    user_id: int
    session_id: str
    current_agent: str
    agent_logs: List[Dict[str, Any]]
    response: str
    sql_query: Optional[str]
    data: Optional[List[Dict[str, Any]]]
    visualization: Optional[Dict[str, Any]]
    metadata: Dict[str, Any]
    should_continue: bool


class AgentOrchestrator:
    """
    Orchestrates multiple AI agents using LangGraph
    """
    
    def __init__(self, user_id: int, domain: Optional[str], session_id: str):
        self.user_id = user_id
        self.domain = domain
        self.session_id = session_id
        
        # Initialize Claude
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-sonnet-4-20250514"
        
        # Initialize agents
        self.welcoming_agent = WelcomingAgent(self.client, self.model)
        self.supervisor_agent = SupervisorAgent(self.client, self.model)
        self.data_manager_agent = DataManagerAgent(self.client, self.model)
        self.data_engineer_agent = DataEngineerAgent(self.client, self.model)
        self.analytics_expert_agent = AnalyticsExpertAgent(self.client, self.model)
        
        # Build graph
        self.graph = self._build_graph()
        
        logger.info(f"AgentOrchestrator initialized for user {user_id}, session {session_id}")
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow"""
        
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("welcoming", self._welcoming_node)
        workflow.add_node("supervisor", self._supervisor_node)
        workflow.add_node("data_manager", self._data_manager_node)
        workflow.add_node("data_engineer", self._data_engineer_node)
        workflow.add_node("analytics_expert", self._analytics_expert_node)
        workflow.add_node("finalize", self._finalize_node)
        
        # Define edges
        workflow.set_entry_point("welcoming")
        
        # Welcoming agent decides if it can handle or route to supervisor
        workflow.add_conditional_edges(
            "welcoming",
            self._route_from_welcoming,
            {
                "end": END,
                "supervisor": "supervisor"
            }
        )
        
        # Supervisor orchestrates team
        workflow.add_conditional_edges(
            "supervisor",
            self._route_from_supervisor,
            {
                "data_manager": "data_manager",
                "data_engineer": "data_engineer",
                "analytics_expert": "analytics_expert",
                "finalize": "finalize"
            }
        )
        
        # Team members return to supervisor
        workflow.add_edge("data_manager", "supervisor")
        workflow.add_edge("data_engineer", "supervisor")
        workflow.add_edge("analytics_expert", "supervisor")
        
        # Finalize ends the workflow
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    async def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process user message through agent workflow
        """
        
        # Get conversation memory
        memory = get_conversation_memory()
        
        # Add user message to memory
        memory.add_message(
            session_id=self.session_id,
            role="user",
            content=message,
            metadata={"domain": self.domain}
        )
        
        # Get conversation context for agents
        context = memory.get_context_for_llm(self.session_id)
        
        # Initialize state
        initial_state = {
            "user_message": message,
            "domain": self.domain,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "current_agent": "welcoming",
            "agent_logs": [],
            "response": "",
            "sql_query": None,
            "data": None,
            "visualization": None,
            "metadata": {"conversation_context": context},
            "should_continue": True
        }
        
        try:
            # Execute workflow
            result = await self.graph.ainvoke(initial_state)
            
            response = result.get("response", "")
            
            # Add assistant response to memory
            memory.add_message(
                session_id=self.session_id,
                role="assistant",
                content=response,
                metadata={"domain": self.domain}
            )
            
            # Track domain usage
            if self.domain:
                memory.track_domain_usage(self.user_id, self.domain)
            
            return {
                "message": response,
                "sql_query": result.get("sql_query"),
                "data": result.get("data"),
                "visualization": result.get("visualization"),
                "agent_logs": result.get("agent_logs", [])
            }
            
        except Exception as e:
            logger.error(f"Error in agent workflow: {e}", exc_info=True)
            return {
                "message": f"I encountered an error processing your request: {str(e)}",
                "agent_logs": []
            }
    
    async def _welcoming_node(self, state: AgentState) -> AgentState:
        """Welcoming Agent node"""
        
        start_time = datetime.now()
        
        result = await self.welcoming_agent.process(
            message=state["user_message"],
            domain=state["domain"]
        )
        
        # Log agent activity
        state["agent_logs"].append({
            "agent_name": "Welcoming Agent",
            "action": "greet_or_route",
            "input": {"message": state["user_message"]},
            "output": result,
            "timestamp": start_time.isoformat(),
            "execution_time": (datetime.now() - start_time).total_seconds()
        })
        
        if result["can_handle"]:
            state["response"] = result["response"]
            state["should_continue"] = False
        else:
            state["should_continue"] = True
        
        return state
    
    async def _supervisor_node(self, state: AgentState) -> AgentState:
        """Supervisor Agent node"""
        
        start_time = datetime.now()
        
        result = await self.supervisor_agent.process(
            message=state["user_message"],
            domain=state["domain"],
            context=state.get("metadata", {})
        )
        
        state["agent_logs"].append({
            "agent_name": "Supervisor Agent",
            "action": "orchestrate",
            "input": {"message": state["user_message"]},
            "output": result,
            "timestamp": start_time.isoformat(),
            "execution_time": (datetime.now() - start_time).total_seconds()
        })
        
        state["current_agent"] = result.get("next_agent", "finalize")
        state["metadata"]["supervisor_plan"] = result.get("plan", "")
        
        return state
    
    async def _data_manager_node(self, state: AgentState) -> AgentState:
        """Data Manager Agent node"""
        
        start_time = datetime.now()
        
        result = await self.data_manager_agent.process(
            message=state["user_message"],
            domain=state["domain"]
        )
        
        state["agent_logs"].append({
            "agent_name": "Data Manager Agent",
            "action": "provide_schema_context",
            "input": {"message": state["user_message"], "domain": state["domain"]},
            "output": result,
            "timestamp": start_time.isoformat(),
            "execution_time": (datetime.now() - start_time).total_seconds()
        })
        
        state["metadata"]["schema_context"] = result.get("schema_info", {})
        
        return state
    
    async def _data_engineer_node(self, state: AgentState) -> AgentState:
        """Data Engineer Agent node"""
        
        start_time = datetime.now()
        
        result = await self.data_engineer_agent.process(
            message=state["user_message"],
            domain=state["domain"],
            schema_context=state["metadata"].get("schema_context", {})
        )
        
        state["agent_logs"].append({
            "agent_name": "Data Engineer Agent",
            "action": "execute_query",
            "input": {"message": state["user_message"]},
            "output": result,
            "timestamp": start_time.isoformat(),
            "execution_time": (datetime.now() - start_time).total_seconds()
        })
        
        state["sql_query"] = result.get("sql_query")
        state["data"] = result.get("data", [])
        state["metadata"]["query_executed"] = True
        
        return state
    
    async def _analytics_expert_node(self, state: AgentState) -> AgentState:
        """Analytics Expert Agent node"""
        
        start_time = datetime.now()
        
        result = await self.analytics_expert_agent.process(
            message=state["user_message"],
            domain=state["domain"],
            data=state.get("data", [])
        )
        
        state["agent_logs"].append({
            "agent_name": "Analytics Expert Agent",
            "action": "analyze_and_visualize",
            "input": {"message": state["user_message"], "data_rows": len(state.get("data", []))},
            "output": result,
            "timestamp": start_time.isoformat(),
            "execution_time": (datetime.now() - start_time).total_seconds()
        })
        
        state["visualization"] = result.get("visualization")
        state["metadata"]["insights"] = result.get("insights", [])
        
        return state
    
    async def _finalize_node(self, state: AgentState) -> AgentState:
        """Finalize response"""
        
        # Supervisor creates final response
        result = await self.supervisor_agent.finalize(
            message=state["user_message"],
            data=state.get("data", []),
            insights=state["metadata"].get("insights", []),
            visualization=state.get("visualization")
        )
        
        state["response"] = result["response"]
        
        return state
    
    def _route_from_welcoming(self, state: AgentState) -> str:
        """Route from welcoming agent"""
        if state["should_continue"]:
            return "supervisor"
        return "end"
    
    def _route_from_supervisor(self, state: AgentState) -> str:
        """Route from supervisor agent"""
        
        next_agent = state.get("current_agent", "finalize")
        
        # Check if work is complete
        if next_agent == "finalize" or not state.get("should_continue", True):
            return "finalize"
        
        return next_agent
