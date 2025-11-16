"""
Domain management API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
import logging

from database.schemas import DomainInfo, DomainListResponse, DomainSelectRequest, DomainType
from api.auth import get_current_user
from database.models import User

logger = logging.getLogger(__name__)
router = APIRouter()

# Domain configurations
DOMAINS = {
    "telecom": {
        "name": DomainType.TELECOM,
        "display_name": "Telecom",
        "description": "Telecommunications industry analytics with network performance, churn, and usage data",
        "icon": "📱",
        "tables": [
            "customer_profiles", "call_records", "data_usage", "billing",
            "network_performance", "churn_data", "device_inventory",
            "complaints", "promotions", "regional_coverage"
        ],
        "kpis": [
            "ARPU (Average Revenue Per User)",
            "Churn Rate",
            "Network Uptime",
            "Data Consumption",
            "Customer Satisfaction Score",
            "Call Drop Rate",
            "Device Upgrade Rate"
        ]
    },
    "banking": {
        "name": DomainType.BANKING,
        "display_name": "Banking",
        "description": "Banking and financial services analytics with transactions, loans, and customer data",
        "icon": "🏦",
        "tables": [
            "accounts", "transactions", "loans", "credit_cards",
            "customers", "branches", "atm_usage", "fraud_alerts",
            "investments", "customer_service_logs"
        ],
        "kpis": [
            "Transaction Volume",
            "Loan Default Rate",
            "Customer Acquisition Cost",
            "Net Promoter Score",
            "Fraud Detection Rate",
            "Average Account Balance",
            "Digital Banking Adoption"
        ]
    },
    "digital_marketing": {
        "name": DomainType.DIGITAL_MARKETING,
        "display_name": "Digital Marketing",
        "description": "Digital marketing analytics with campaigns, conversions, and engagement metrics",
        "icon": "📊",
        "tables": [
            "campaigns", "ad_performance", "website_traffic", "conversions",
            "email_metrics", "social_media", "seo_rankings", "customer_journey",
            "ab_tests", "budgets"
        ],
        "kpis": [
            "Click-Through Rate (CTR)",
            "Conversion Rate",
            "Customer Acquisition Cost (CAC)",
            "Return on Ad Spend (ROAS)",
            "Engagement Rate",
            "Bounce Rate",
            "Cost Per Click (CPC)"
        ]
    },
    "healthcare": {
        "name": DomainType.HEALTHCARE,
        "display_name": "Healthcare",
        "description": "Healthcare analytics with patient data, appointments, and treatment outcomes",
        "icon": "🏥",
        "tables": [
            "patients", "appointments", "medical_records", "prescriptions",
            "lab_results", "staff", "departments", "billing",
            "insurance_claims", "equipment"
        ],
        "kpis": [
            "Patient Wait Time",
            "Bed Occupancy Rate",
            "Readmission Rate",
            "Treatment Success Rate",
            "Staff Utilization",
            "Patient Satisfaction",
            "Average Length of Stay"
        ]
    },
    "fmcg": {
        "name": DomainType.FMCG,
        "display_name": "FMCG",
        "description": "Fast-Moving Consumer Goods analytics with sales, inventory, and distribution data",
        "icon": "🛒",
        "tables": [
            "products", "inventory", "sales", "distributors",
            "retailers", "promotions", "supply_chain", "market_research",
            "customer_feedback", "pricing"
        ],
        "kpis": [
            "Sales Velocity",
            "Inventory Turnover",
            "Market Share",
            "Distribution Coverage",
            "Profit Margin",
            "Stock-Out Rate",
            "Promotion Effectiveness"
        ]
    }
}


@router.get("", response_model=DomainListResponse)
async def get_domains(current_user: User = Depends(get_current_user)):
    """Get list of all available domains"""
    
    domain_list = [
        DomainInfo(**domain_data)
        for domain_data in DOMAINS.values()
    ]
    
    return DomainListResponse(domains=domain_list)


@router.get("/{domain_name}", response_model=DomainInfo)
async def get_domain(
    domain_name: str,
    current_user: User = Depends(get_current_user)
):
    """Get specific domain information"""
    
    if domain_name not in DOMAINS:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    return DomainInfo(**DOMAINS[domain_name])


@router.post("/select")
async def select_domain(
    request: DomainSelectRequest,
    current_user: User = Depends(get_current_user)
):
    """Select active domain for user session"""
    
    domain_key = request.domain.value
    
    if domain_key not in DOMAINS:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    logger.info(f"User {current_user.username} selected domain: {domain_key}")
    
    return {
        "message": f"Domain switched to {DOMAINS[domain_key]['display_name']}",
        "domain": DomainInfo(**DOMAINS[domain_key])
    }


@router.get("/{domain_name}/schema")
async def get_domain_schema(
    domain_name: str,
    current_user: User = Depends(get_current_user)
):
    """Get database schema for specific domain"""
    
    if domain_name not in DOMAINS:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    # This would return actual schema from database
    # For now, returning placeholder
    
    return {
        "domain": domain_name,
        "tables": DOMAINS[domain_name]["tables"],
        "schema": "Schema details would be loaded from database"
    }
