"""
Welcoming Agent - Handles greetings and general queries
"""

import logging
from typing import Dict, Any, Optional
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class WelcomingAgent:
    """
    Handles greetings, navigation, and general platform queries
    Routes business queries to Data Analytics Supervisor
    """
    
    def __init__(self, client: Anthropic, model: str):
        self.client = client
        self.model = model
        self.name = "Welcoming Agent"
    
    async def process(self, message: str, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Process incoming message and decide if can handle or route
        """
        
        system_prompt = """You are the Welcoming Agent for COGNIX AI, an intelligent data analytics platform.

Your responsibilities:
1. Greet users warmly and professionally
2. Answer general questions about the platform (features, domains, how to use)
3. Help with navigation and platform understanding
4. Identify if a query requires data analysis

For these types of queries, handle them yourself:
- Greetings (hello, hi, how are you)
- Platform questions (what can you do, what domains do you support)
- Navigation help (how do I..., where can I find...)
- General information requests about the platform

For these types of queries, indicate you CANNOT handle them (route to supervisor):
- Specific data queries (show me sales data, what's the churn rate)
- Analytics requests (predict, analyze, find trends)
- SQL or database queries
- Visualization requests
- Any domain-specific business questions

Respond in JSON format:
{
    "can_handle": true/false,
    "response": "your response if you can handle it",
    "reason": "why routing to supervisor if needed"
}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.7,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"User message: {message}\nCurrent domain: {domain or 'None selected'}"
                }]
            )
            
            # Parse response
            import json
            result = json.loads(response.content[0].text)
            
            logger.info(f"Welcoming Agent - Can handle: {result['can_handle']}")
            return result
            
        except Exception as e:
            logger.error(f"Welcoming Agent error: {e}")
            return {
                "can_handle": False,
                "response": "",
                "reason": "Error processing message"
            }
