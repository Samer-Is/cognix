"""
Supervisor Agent - Orchestrates team and validates outputs
"""

import logging
from typing import Dict, Any, Optional, List
from anthropic import Anthropic
import json

logger = logging.getLogger(__name__)


class SupervisorAgent:
    """
    Orchestrates the data analytics team
    Creates execution plans, validates outputs, manages feedback loops
    """
    
    def __init__(self, client: Anthropic, model: str):
        self.client = client
        self.model = model
        self.name = "Supervisor Agent"
    
    async def process(
        self,
        message: str,
        domain: Optional[str],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create execution plan and decide which agent to involve
        """
        
        system_prompt = """You are the Data Analytics Supervisor for COGNIX AI.

Your responsibilities:
1. Analyze user queries to understand intent
2. Create execution plans for complex queries
3. Decide which team members to involve (Data Manager, Data Engineer, Analytics Expert)
4. Validate outputs from team members
5. Implement feedback loops if answers are inaccurate

Available team members:
- Data Manager: Knows all database schemas, tables, columns, relationships
- Data Engineer: Converts natural language to SQL, executes queries
- Analytics Expert: Performs analysis, generates insights, creates visualizations

For each query, create a plan with these steps:
1. If query needs schema understanding → involve Data Manager
2. If query needs data retrieval → involve Data Engineer
3. If query needs analysis/visualization → involve Analytics Expert
4. Then finalize the response

Respond in JSON format:
{
    "plan": "step by step plan",
    "next_agent": "data_manager" | "data_engineer" | "analytics_expert" | "finalize",
    "reasoning": "why this agent is needed"
}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.3,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"""User query: {message}
Domain: {domain}
Current context: {json.dumps(context, indent=2)}

What's the next step in processing this query?"""
                }]
            )
            
            result = json.loads(response.content[0].text)
            logger.info(f"Supervisor - Next agent: {result.get('next_agent')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Supervisor error: {e}")
            return {
                "plan": "Error creating plan",
                "next_agent": "finalize",
                "reasoning": str(e)
            }
    
    async def finalize(
        self,
        message: str,
        data: List[Dict[str, Any]],
        insights: List[str],
        visualization: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Create final response combining all team outputs
        """
        
        system_prompt = """You are the Data Analytics Supervisor finalizing a response.

Create a comprehensive, user-friendly response that:
1. Directly answers the user's question
2. Highlights key insights found in the data
3. Explains the visualization if present
4. Provides actionable recommendations if appropriate

Be conversational, clear, and insightful. Format with markdown for readability."""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.7,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"""User query: {message}

Data retrieved: {len(data)} rows
Insights: {json.dumps(insights, indent=2)}
Visualization: {json.dumps(visualization, indent=2) if visualization else 'None'}

Create a final response for the user."""
                }]
            )
            
            return {
                "response": response.content[0].text
            }
            
        except Exception as e:
            logger.error(f"Supervisor finalize error: {e}")
            return {
                "response": f"Based on the analysis of {len(data)} data points, here are the findings."
            }
