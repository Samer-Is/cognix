"""
Data Manager Agent - Domain expert on schemas and data relationships
"""

import logging
from typing import Dict, Any, Optional
from anthropic import Anthropic
import json

logger = logging.getLogger(__name__)


# Domain schema information
DOMAIN_SCHEMAS = {
    "telecom": {
        "tables": {
            "customer_profiles": ["customer_id", "name", "phone", "plan_type", "join_date", "status"],
            "call_records": ["call_id", "customer_id", "duration", "call_type", "timestamp", "cost"],
            "data_usage": ["usage_id", "customer_id", "data_mb", "date", "app_category"],
            "billing": ["bill_id", "customer_id", "amount", "due_date", "paid", "payment_date"],
            "network_performance": ["metric_id", "region", "uptime_pct", "avg_speed_mbps", "date"],
            "churn_data": ["customer_id", "churn_date", "reason", "last_interaction"],
            "device_inventory": ["device_id", "customer_id", "model", "purchase_date"],
            "complaints": ["complaint_id", "customer_id", "category", "status", "date"],
            "promotions": ["promo_id", "name", "discount_pct", "start_date", "end_date"],
            "regional_coverage": ["region", "towers", "coverage_pct", "subscribers"]
        },
        "kpis": ["ARPU", "Churn Rate", "Network Uptime", "Data Consumption", "Customer Satisfaction"]
    },
    "banking": {
        "tables": {
            "accounts": ["account_id", "customer_id", "account_type", "balance", "opening_date"],
            "transactions": ["transaction_id", "account_id", "type", "amount", "date", "merchant"],
            "loans": ["loan_id", "customer_id", "amount", "interest_rate", "status", "issue_date"],
            "credit_cards": ["card_id", "customer_id", "credit_limit", "balance", "due_date"],
            "customers": ["customer_id", "name", "email", "phone", "join_date", "segment"],
            "branches": ["branch_id", "name", "location", "employees", "transactions_count"],
            "atm_usage": ["usage_id", "customer_id", "atm_id", "amount", "timestamp"],
            "fraud_alerts": ["alert_id", "transaction_id", "risk_score", "status", "date"],
            "investments": ["investment_id", "customer_id", "type", "amount", "returns_pct"],
            "customer_service_logs": ["log_id", "customer_id", "issue", "resolution", "date"]
        },
        "kpis": ["Transaction Volume", "Loan Default Rate", "CAC", "NPS", "Fraud Detection Rate"]
    },
    "digital_marketing": {
        "tables": {
            "campaigns": ["campaign_id", "name", "budget", "start_date", "end_date", "channel"],
            "ad_performance": ["ad_id", "campaign_id", "impressions", "clicks", "conversions", "date"],
            "website_traffic": ["session_id", "source", "page_views", "duration", "bounce", "date"],
            "conversions": ["conversion_id", "session_id", "value", "type", "date"],
            "email_metrics": ["email_id", "campaign_id", "sent", "opened", "clicked", "date"],
            "social_media": ["post_id", "platform", "engagement", "reach", "date"],
            "seo_rankings": ["keyword", "position", "search_volume", "date"],
            "customer_journey": ["journey_id", "customer_id", "touchpoints", "conversion_date"],
            "ab_tests": ["test_id", "variant", "conversions", "sample_size", "date"],
            "budgets": ["month", "channel", "allocated", "spent", "roi"]
        },
        "kpis": ["CTR", "Conversion Rate", "CAC", "ROAS", "Engagement Rate", "Bounce Rate"]
    },
    "healthcare": {
        "tables": {
            "patients": ["patient_id", "name", "age", "gender", "contact", "insurance"],
            "appointments": ["appointment_id", "patient_id", "doctor_id", "date", "status"],
            "medical_records": ["record_id", "patient_id", "diagnosis", "treatment", "date"],
            "prescriptions": ["prescription_id", "patient_id", "medication", "dosage", "date"],
            "lab_results": ["result_id", "patient_id", "test_type", "result", "date"],
            "staff": ["staff_id", "name", "role", "department", "hire_date"],
            "departments": ["dept_id", "name", "head", "bed_count", "occupancy"],
            "billing": ["bill_id", "patient_id", "amount", "insurance_covered", "date"],
            "insurance_claims": ["claim_id", "patient_id", "amount", "status", "date"],
            "equipment": ["equipment_id", "name", "department", "status", "maintenance_date"]
        },
        "kpis": ["Patient Wait Time", "Bed Occupancy", "Readmission Rate", "Staff Utilization"]
    },
    "fmcg": {
        "tables": {
            "products": ["product_id", "name", "category", "price", "cost", "launch_date"],
            "inventory": ["sku", "product_id", "warehouse", "quantity", "last_updated"],
            "sales": ["sale_id", "product_id", "retailer_id", "quantity", "revenue", "date"],
            "distributors": ["distributor_id", "name", "region", "performance_score"],
            "retailers": ["retailer_id", "name", "location", "type", "sales_volume"],
            "promotions": ["promo_id", "product_id", "discount_pct", "start_date", "end_date"],
            "supply_chain": ["shipment_id", "product_id", "origin", "destination", "date"],
            "market_research": ["survey_id", "product_id", "sentiment", "responses", "date"],
            "customer_feedback": ["feedback_id", "product_id", "rating", "comment", "date"],
            "pricing": ["product_id", "region", "price", "competitor_price", "date"]
        },
        "kpis": ["Sales Velocity", "Inventory Turnover", "Market Share", "Profit Margin"]
    }
}


class DataManagerAgent:
    """
    Expert on all database schemas across domains
    Provides metadata and data context to other agents
    """
    
    def __init__(self, client: Anthropic, model: str):
        self.client = client
        self.model = model
        self.name = "Data Manager Agent"
    
    async def process(
        self,
        message: str,
        domain: Optional[str]
    ) -> Dict[str, Any]:
        """
        Provide schema context and data relationships for the query
        """
        
        if not domain or domain not in DOMAIN_SCHEMAS:
            return {
                "schema_info": {},
                "error": "Domain not specified or invalid"
            }
        
        schema = DOMAIN_SCHEMAS[domain]
        
        system_prompt = f"""You are the Data Manager for COGNIX AI, expert on the {domain} domain database.

Available tables and columns:
{json.dumps(schema['tables'], indent=2)}

Key Performance Indicators:
{', '.join(schema['kpis'])}

Your task:
1. Identify which tables are needed for the user's query
2. Specify the relevant columns
3. Describe any relationships between tables
4. Suggest KPIs that could be calculated

Respond in JSON format:
{{
    "relevant_tables": ["table1", "table2"],
    "key_columns": ["col1", "col2"],
    "relationships": "description of how tables relate",
    "suggested_kpis": ["kpi1", "kpi2"],
    "notes": "any additional context"
}}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.2,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"User query: {message}\n\nWhat schema information is needed?"
                }]
            )
            
            result = json.loads(response.content[0].text)
            result["domain_schema"] = schema
            
            logger.info(f"Data Manager - Relevant tables: {result.get('relevant_tables')}")
            
            return {"schema_info": result}
            
        except Exception as e:
            logger.error(f"Data Manager error: {e}")
            return {
                "schema_info": {
                    "error": str(e),
                    "domain_schema": schema
                }
            }
