"""
Data Engineer Agent - Converts natural language to SQL and executes queries
"""

import logging
from typing import Dict, Any, Optional, List
from anthropic import Anthropic
import json

logger = logging.getLogger(__name__)


class DataEngineerAgent:
    """
    Converts natural language queries to SQL
    Executes data retrieval operations
    Handles data transformations and aggregations
    """
    
    def __init__(self, client: Anthropic, model: str):
        self.client = client
        self.model = model
        self.name = "Data Engineer Agent"
    
    async def process(
        self,
        message: str,
        domain: Optional[str],
        schema_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate and execute SQL query based on user request
        """
        
        system_prompt = f"""You are the Data Engineer for COGNIX AI.

Your responsibilities:
1. Convert natural language queries to SQL
2. Use the schema information provided
3. Write optimized, correct SQL queries
4. Handle aggregations, joins, and filtering properly

Schema context:
{json.dumps(schema_context, indent=2)}

Rules:
- Use PostgreSQL syntax
- Always include appropriate WHERE clauses for filtering
- Use JOINs when multiple tables are needed
- Include ORDER BY and LIMIT for large result sets
- Handle dates properly
- Use aggregate functions (COUNT, SUM, AVG, etc.) when appropriate

Respond in JSON format:
{{
    "sql_query": "SELECT ... FROM ...",
    "explanation": "what the query does",
    "estimated_rows": approximate number
}}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.1,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"User query: {message}\n\nGenerate the SQL query."
                }]
            )
            
            result = json.loads(response.content[0].text)
            sql_query = result.get("sql_query", "")
            
            logger.info(f"Data Engineer - Generated SQL: {sql_query[:100]}...")
            
            # Execute query (in real implementation, this would query the database)
            # For now, returning mock data
            data = await self._execute_query(sql_query, domain)
            
            return {
                "sql_query": sql_query,
                "explanation": result.get("explanation", ""),
                "data": data
            }
            
        except Exception as e:
            logger.error(f"Data Engineer error: {e}")
            return {
                "sql_query": None,
                "explanation": f"Error: {str(e)}",
                "data": []
            }
    
    async def _execute_query(self, sql_query: str, domain: Optional[str]) -> List[Dict[str, Any]]:
        """
        Execute SQL query and return results
        In production, this would connect to the actual database
        """
        
        # Mock data for demonstration
        # In real implementation, use SQLAlchemy to execute query
        
        if not sql_query:
            return []
        
        # Return mock data based on query type
        if "COUNT" in sql_query.upper():
            return [{"count": 1234}]
        elif "AVG" in sql_query.upper():
            return [{"average": 45.67}]
        elif "SUM" in sql_query.upper():
            return [{"total": 98765.43}]
        else:
            # Return sample rows
            return [
                {"id": 1, "value": 100, "date": "2024-11-01"},
                {"id": 2, "value": 150, "date": "2024-11-02"},
                {"id": 3, "value": 120, "date": "2024-11-03"},
                {"id": 4, "value": 180, "date": "2024-11-04"},
                {"id": 5, "value": 200, "date": "2024-11-05"}
            ]
