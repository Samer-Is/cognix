"""
Analytics Expert Agent - Performs analysis and creates visualizations
"""

import logging
from typing import Dict, Any, Optional, List
from anthropic import Anthropic
import json

logger = logging.getLogger(__name__)


class AnalyticsExpertAgent:
    """
    Performs statistical analysis and predictive modeling
    Generates insights, trends, and recommendations
    Creates visualization specifications
    Detects anomalies and patterns
    """
    
    def __init__(self, client: Anthropic, model: str):
        self.client = client
        self.model = model
        self.name = "Analytics Expert Agent"
    
    async def process(
        self,
        message: str,
        domain: Optional[str],
        data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze data and generate insights with visualizations
        """
        
        system_prompt = """You are the Analytics Expert for COGNIX AI.

Your responsibilities:
1. Analyze data to find patterns, trends, and anomalies
2. Generate actionable insights
3. Create visualization specifications for frontend rendering
4. Provide statistical analysis and predictions when appropriate
5. Make business recommendations

Available visualization types:
- line: For time series and trends
- bar: For comparisons across categories
- pie: For proportions and distributions
- scatter: For correlations
- heatmap: For multi-dimensional data
- table: For detailed data view

Visualization spec format:
{
    "type": "line",
    "title": "Chart Title",
    "data": [{"x": "label", "y": value}, ...],
    "x_axis": "X Axis Label",
    "y_axis": "Y Axis Label",
    "colors": ["#color1", "#color2"]
}

Respond in JSON format:
{
    "insights": ["insight 1", "insight 2", "insight 3"],
    "visualization": {visualization spec},
    "recommendations": ["recommendation 1", "recommendation 2"],
    "summary": "brief summary of findings"
}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.5,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"""User query: {message}

Data to analyze:
{json.dumps(data[:10], indent=2) if data else "No data available"}
Total rows: {len(data)}

Provide insights and visualization."""
                }]
            )
            
            result = json.loads(response.content[0].text)
            
            logger.info(f"Analytics Expert - Generated {len(result.get('insights', []))} insights")
            
            return result
            
        except Exception as e:
            logger.error(f"Analytics Expert error: {e}")
            
            # Fallback visualization
            if data:
                return {
                    "insights": [
                        f"Analyzed {len(data)} data points",
                        "Data shows variation across the dataset"
                    ],
                    "visualization": {
                        "type": "table",
                        "title": "Data Overview",
                        "data": data[:10]
                    },
                    "recommendations": ["Further analysis recommended"],
                    "summary": "Basic analysis completed"
                }
            else:
                return {
                    "insights": ["No data available for analysis"],
                    "visualization": None,
                    "recommendations": [],
                    "summary": "No data to analyze"
                }
