"""
Data generation script for all 5 domains
Generates realistic CSV data for demo purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import argparse
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Create data directory
DATA_DIR = Path("../data/generated")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_telecom_data():
    """Generate Telecom domain data"""
    print("📱 Generating Telecom data...")
    
    n_customers = 1000
    
    # Customer profiles
    customers = pd.DataFrame({
        'customer_id': range(1, n_customers + 1),
        'name': [f"Customer_{i}" for i in range(1, n_customers + 1)],
        'phone': [f"+1{random.randint(1000000000, 9999999999)}" for _ in range(n_customers)],
        'plan_type': np.random.choice(['Basic', 'Premium', 'Enterprise'], n_customers, p=[0.5, 0.3, 0.2]),
        'join_date': [datetime.now() - timedelta(days=random.randint(1, 1000)) for _ in range(n_customers)],
        'status': np.random.choice(['Active', 'Inactive'], n_customers, p=[0.9, 0.1])
    })
    customers.to_csv(DATA_DIR / "telecom_customer_profiles.csv", index=False)
    
    # Call records
    n_calls = 5000
    calls = pd.DataFrame({
        'call_id': range(1, n_calls + 1),
        'customer_id': np.random.randint(1, n_customers + 1, n_calls),
        'duration': np.random.randint(1, 3600, n_calls),
        'call_type': np.random.choice(['Voice', 'Video', 'Conference'], n_calls),
        'timestamp': [datetime.now() - timedelta(days=random.randint(1, 30), hours=random.randint(0, 23)) for _ in range(n_calls)],
        'cost': np.random.uniform(0.05, 5.0, n_calls).round(2)
    })
    calls.to_csv(DATA_DIR / "telecom_call_records.csv", index=False)
    
    # Data usage
    n_usage = 3000
    data_usage = pd.DataFrame({
        'usage_id': range(1, n_usage + 1),
        'customer_id': np.random.randint(1, n_customers + 1, n_usage),
        'data_mb': np.random.randint(10, 10000, n_usage),
        'date': [datetime.now() - timedelta(days=random.randint(1, 30)) for _ in range(n_usage)],
        'app_category': np.random.choice(['Social', 'Streaming', 'Gaming', 'Browsing', 'Work'], n_usage)
    })
    data_usage.to_csv(DATA_DIR / "telecom_data_usage.csv", index=False)
    
    print(f"✅ Generated Telecom data: {len(customers)} customers, {len(calls)} calls, {len(data_usage)} usage records")


def generate_banking_data():
    """Generate Banking domain data"""
    print("🏦 Generating Banking data...")
    
    n_customers = 800
    
    # Customers
    customers = pd.DataFrame({
        'customer_id': range(1, n_customers + 1),
        'name': [f"Customer_{i}" for i in range(1, n_customers + 1)],
        'email': [f"customer{i}@email.com" for i in range(1, n_customers + 1)],
        'phone': [f"+1{random.randint(1000000000, 9999999999)}" for _ in range(n_customers)],
        'join_date': [datetime.now() - timedelta(days=random.randint(1, 2000)) for _ in range(n_customers)],
        'segment': np.random.choice(['Retail', 'Premium', 'Business'], n_customers, p=[0.6, 0.3, 0.1])
    })
    customers.to_csv(DATA_DIR / "banking_customers.csv", index=False)
    
    # Accounts
    n_accounts = 1200
    accounts = pd.DataFrame({
        'account_id': range(1, n_accounts + 1),
        'customer_id': np.random.randint(1, n_customers + 1, n_accounts),
        'account_type': np.random.choice(['Checking', 'Savings', 'Credit'], n_accounts),
        'balance': np.random.uniform(100, 100000, n_accounts).round(2),
        'opening_date': [datetime.now() - timedelta(days=random.randint(1, 2000)) for _ in range(n_accounts)]
    })
    accounts.to_csv(DATA_DIR / "banking_accounts.csv", index=False)
    
    # Transactions
    n_transactions = 10000
    transactions = pd.DataFrame({
        'transaction_id': range(1, n_transactions + 1),
        'account_id': np.random.randint(1, n_accounts + 1, n_transactions),
        'type': np.random.choice(['Deposit', 'Withdrawal', 'Transfer', 'Payment'], n_transactions),
        'amount': np.random.uniform(10, 5000, n_transactions).round(2),
        'date': [datetime.now() - timedelta(days=random.randint(1, 90)) for _ in range(n_transactions)],
        'merchant': [f"Merchant_{random.randint(1, 100)}" for _ in range(n_transactions)]
    })
    transactions.to_csv(DATA_DIR / "banking_transactions.csv", index=False)
    
    print(f"✅ Generated Banking data: {len(customers)} customers, {len(accounts)} accounts, {len(transactions)} transactions")


def generate_digital_marketing_data():
    """Generate Digital Marketing domain data"""
    print("📊 Generating Digital Marketing data...")
    
    n_campaigns = 50
    
    # Campaigns
    campaigns = pd.DataFrame({
        'campaign_id': range(1, n_campaigns + 1),
        'name': [f"Campaign_{i}" for i in range(1, n_campaigns + 1)],
        'budget': np.random.uniform(1000, 50000, n_campaigns).round(2),
        'start_date': [datetime.now() - timedelta(days=random.randint(30, 180)) for _ in range(n_campaigns)],
        'end_date': [datetime.now() + timedelta(days=random.randint(1, 90)) for _ in range(n_campaigns)],
        'channel': np.random.choice(['Google Ads', 'Facebook', 'Instagram', 'LinkedIn', 'Twitter'], n_campaigns)
    })
    campaigns.to_csv(DATA_DIR / "marketing_campaigns.csv", index=False)
    
    # Ad Performance
    n_ads = 500
    ads = pd.DataFrame({
        'ad_id': range(1, n_ads + 1),
        'campaign_id': np.random.randint(1, n_campaigns + 1, n_ads),
        'impressions': np.random.randint(1000, 100000, n_ads),
        'clicks': np.random.randint(10, 5000, n_ads),
        'conversions': np.random.randint(0, 500, n_ads),
        'date': [datetime.now() - timedelta(days=random.randint(1, 60)) for _ in range(n_ads)]
    })
    ads['ctr'] = (ads['clicks'] / ads['impressions'] * 100).round(2)
    ads['conversion_rate'] = (ads['conversions'] / ads['clicks'] * 100).round(2)
    ads.to_csv(DATA_DIR / "marketing_ad_performance.csv", index=False)
    
    print(f"✅ Generated Marketing data: {len(campaigns)} campaigns, {len(ads)} ad performance records")


def generate_healthcare_data():
    """Generate Healthcare domain data"""
    print("🏥 Generating Healthcare data...")
    
    n_patients = 600
    
    # Patients
    patients = pd.DataFrame({
        'patient_id': range(1, n_patients + 1),
        'name': [f"Patient_{i}" for i in range(1, n_patients + 1)],
        'age': np.random.randint(1, 90, n_patients),
        'gender': np.random.choice(['M', 'F', 'O'], n_patients),
        'contact': [f"+1{random.randint(1000000000, 9999999999)}" for _ in range(n_patients)],
        'insurance': np.random.choice(['Medicare', 'Private', 'Medicaid', 'None'], n_patients)
    })
    patients.to_csv(DATA_DIR / "healthcare_patients.csv", index=False)
    
    # Appointments
    n_appointments = 2000
    appointments = pd.DataFrame({
        'appointment_id': range(1, n_appointments + 1),
        'patient_id': np.random.randint(1, n_patients + 1, n_appointments),
        'doctor_id': np.random.randint(1, 51, n_appointments),
        'date': [datetime.now() - timedelta(days=random.randint(1, 180)) for _ in range(n_appointments)],
        'status': np.random.choice(['Completed', 'Scheduled', 'Cancelled'], n_appointments, p=[0.7, 0.2, 0.1])
    })
    appointments.to_csv(DATA_DIR / "healthcare_appointments.csv", index=False)
    
    print(f"✅ Generated Healthcare data: {len(patients)} patients, {len(appointments)} appointments")


def generate_fmcg_data():
    """Generate FMCG domain data"""
    print("🛒 Generating FMCG data...")
    
    n_products = 200
    
    # Products
    products = pd.DataFrame({
        'product_id': range(1, n_products + 1),
        'name': [f"Product_{i}" for i in range(1, n_products + 1)],
        'category': np.random.choice(['Food', 'Beverage', 'Personal Care', 'Home Care', 'Snacks'], n_products),
        'price': np.random.uniform(1, 100, n_products).round(2),
        'cost': np.random.uniform(0.5, 50, n_products).round(2),
        'launch_date': [datetime.now() - timedelta(days=random.randint(1, 1000)) for _ in range(n_products)]
    })
    products.to_csv(DATA_DIR / "fmcg_products.csv", index=False)
    
    # Sales
    n_sales = 5000
    sales = pd.DataFrame({
        'sale_id': range(1, n_sales + 1),
        'product_id': np.random.randint(1, n_products + 1, n_sales),
        'retailer_id': np.random.randint(1, 101, n_sales),
        'quantity': np.random.randint(1, 100, n_sales),
        'revenue': np.random.uniform(10, 1000, n_sales).round(2),
        'date': [datetime.now() - timedelta(days=random.randint(1, 90)) for _ in range(n_sales)]
    })
    sales.to_csv(DATA_DIR / "fmcg_sales.csv", index=False)
    
    # Inventory
    n_inventory = 1000
    inventory = pd.DataFrame({
        'sku': range(1, n_inventory + 1),
        'product_id': np.random.randint(1, n_products + 1, n_inventory),
        'warehouse': [f"WH_{random.randint(1, 10)}" for _ in range(n_inventory)],
        'quantity': np.random.randint(0, 1000, n_inventory),
        'last_updated': [datetime.now() - timedelta(days=random.randint(1, 30)) for _ in range(n_inventory)]
    })
    inventory.to_csv(DATA_DIR / "fmcg_inventory.csv", index=False)
    
    print(f"✅ Generated FMCG data: {len(products)} products, {len(sales)} sales, {len(inventory)} inventory records")


def main():
    parser = argparse.ArgumentParser(description='Generate demo data for COGNIX AI')
    parser.add_argument('--domain', type=str, choices=['telecom', 'banking', 'digital_marketing', 'healthcare', 'fmcg', 'all'],
                        default='all', help='Domain to generate data for')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("COGNIX AI - Data Generation")
    print("=" * 50)
    print()
    
    if args.domain in ['telecom', 'all']:
        generate_telecom_data()
    
    if args.domain in ['banking', 'all']:
        generate_banking_data()
    
    if args.domain in ['digital_marketing', 'all']:
        generate_digital_marketing_data()
    
    if args.domain in ['healthcare', 'all']:
        generate_healthcare_data()
    
    if args.domain in ['fmcg', 'all']:
        generate_fmcg_data()
    
    print()
    print("=" * 50)
    print(f"✅ Data generation complete! Files saved to: {DATA_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
