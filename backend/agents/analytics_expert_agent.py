"""
Analytics Expert Agent - Generates insights and recommendations
"""

import logging
from typing import Dict, Any, Optional, List
from anthropic import Anthropic
import json
from services.analytics_engine import AnalyticsEngine
from services.sentiment_analyzer import SentimentAnalyzer
from services.alert_service import AlertService

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
            # First, run advanced analytics
            analytics_results = {}
            alerts = []
            
            if data and len(data) > 2:
                # Try to find numeric columns
                numeric_columns = []
                text_columns = []
                
                for key in data[0].keys():
                    try:
                        float(data[0][key])
                        numeric_columns.append(key)
                    except (ValueError, TypeError):
                        # Check if it's a text column
                        if isinstance(data[0][key], str) and len(data[0][key]) > 20:
                            text_columns.append(key)
                
                # Detect anomalies if we have numeric data
                if numeric_columns:
                    main_metric = numeric_columns[0]
                    analytics_results['anomalies'] = AnalyticsEngine.detect_anomalies(
                        data, main_metric, threshold=2.0
                    )
                    
                    # Generate alerts for anomalies
                    alert_result = AlertService.generate_comprehensive_alerts(
                        data, main_metric, domain=domain
                    )
                    if alert_result['total_alerts'] > 0:
                        analytics_results['alerts'] = alert_result
                        alerts = alert_result['alerts'][:5]  # Top 5 alerts
                    
                    # Forecast if enough data
                    if len(data) >= 7:
                        analytics_results['forecast'] = AnalyticsEngine.forecast_trend(
                            data, main_metric, periods=7
                        )
                
                # Sentiment analysis if we have text columns
                if text_columns:
                    sentiment_result = SentimentAnalyzer.analyze_dataframe_column(
                        data, text_columns[0]
                    )
                    if "error" not in sentiment_result:
                        analytics_results['sentiment'] = sentiment_result
                
                # Segment analysis if we have categorical columns
                categorical_cols = [k for k in data[0].keys() if k not in numeric_columns and k not in text_columns]
                if categorical_cols and numeric_columns:
                    analytics_results['segments'] = AnalyticsEngine.segment_analysis(
                        data, categorical_cols[0], numeric_columns[0]
                    )
            
            # Now get AI insights
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

Advanced analytics results:
{json.dumps(analytics_results, indent=2)}

Provide insights and visualization."""
                }]
            )
            
            result = json.loads(response.content[0].text)
            
            # Add analytics results to response
            result['advanced_analytics'] = analytics_results
            
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
