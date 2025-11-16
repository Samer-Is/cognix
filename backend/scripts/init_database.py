"""
Database initialization and CSV data loader
Loads generated CSV files into PostgreSQL database
"""

import asyncio
import pandas as pd
from pathlib import Path
from sqlalchemy import text
from database.connection import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_DIR = Path("../data/generated")


async def create_tables():
    """Create database tables from CSV structure"""
    
    async with engine.begin() as conn:
        # Telecom tables
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS telecom_customer_profiles (
                customer_id INTEGER PRIMARY KEY,
                name VARCHAR(255),
                phone VARCHAR(50),
                plan_type VARCHAR(50),
                join_date TIMESTAMP,
                status VARCHAR(50)
            )
        """))
        
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS telecom_call_records (
                call_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                duration INTEGER,
                call_type VARCHAR(50),
                timestamp TIMESTAMP,
                cost DECIMAL(10,2)
            )
        """))
        
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS telecom_data_usage (
                usage_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                data_mb INTEGER,
                date TIMESTAMP,
                app_category VARCHAR(50)
            )
        """))
        
        # Banking tables
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS banking_customers (
                customer_id INTEGER PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(50),
                join_date TIMESTAMP,
                segment VARCHAR(50)
            )
        """))
        
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS banking_accounts (
                account_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                account_type VARCHAR(50),
                balance DECIMAL(15,2),
                opening_date TIMESTAMP
            )
        """))
        
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS banking_transactions (
                transaction_id INTEGER PRIMARY KEY,
                account_id INTEGER,
                type VARCHAR(50),
                amount DECIMAL(15,2),
                date TIMESTAMP,
                merchant VARCHAR(255)
            )
        """))
        
        # Marketing tables
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS marketing_campaigns (
                campaign_id INTEGER PRIMARY KEY,
                name VARCHAR(255),
                budget DECIMAL(15,2),
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                channel VARCHAR(100)
            )
        """))
        
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS marketing_ad_performance (
                ad_id INTEGER PRIMARY KEY,
                campaign_id INTEGER,
                impressions INTEGER,
                clicks INTEGER,
                conversions INTEGER,
                date TIMESTAMP,
                ctr DECIMAL(10,2),
                conversion_rate DECIMAL(10,2)
            )
        """))
        
        # Healthcare tables
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS healthcare_patients (
                patient_id INTEGER PRIMARY KEY,
                name VARCHAR(255),
                age INTEGER,
                gender CHAR(1),
                contact VARCHAR(50),
                insurance VARCHAR(100)
            )
        """))
        
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS healthcare_appointments (
                appointment_id INTEGER PRIMARY KEY,
                patient_id INTEGER,
                doctor_id INTEGER,
                date TIMESTAMP,
                status VARCHAR(50)
            )
        """))
        
        # FMCG tables
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fmcg_products (
                product_id INTEGER PRIMARY KEY,
                name VARCHAR(255),
                category VARCHAR(100),
                price DECIMAL(10,2),
                cost DECIMAL(10,2),
                launch_date TIMESTAMP
            )
        """))
        
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fmcg_sales (
                sale_id INTEGER PRIMARY KEY,
                product_id INTEGER,
                retailer_id INTEGER,
                quantity INTEGER,
                revenue DECIMAL(15,2),
                date TIMESTAMP
            )
        """))
        
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fmcg_inventory (
                sku INTEGER PRIMARY KEY,
                product_id INTEGER,
                warehouse VARCHAR(50),
                quantity INTEGER,
                last_updated TIMESTAMP
            )
        """))
        
        logger.info("✅ All tables created successfully")


async def load_csv_data():
    """Load CSV files into database"""
    
    csv_files = list(DATA_DIR.glob("*.csv"))
    
    for csv_file in csv_files:
        table_name = csv_file.stem
        logger.info(f"Loading {table_name}...")
        
        try:
            df = pd.read_csv(csv_file)
            
            async with engine.begin() as conn:
                # Convert DataFrame to SQL
                for _, row in df.iterrows():
                    columns = ', '.join(row.index)
                    placeholders = ', '.join([f":{col}" for col in row.index])
                    
                    insert_sql = f"""
                        INSERT INTO {table_name} ({columns})
                        VALUES ({placeholders})
                        ON CONFLICT DO NOTHING
                    """
                    
                    await conn.execute(text(insert_sql), row.to_dict())
            
            logger.info(f"✅ Loaded {len(df)} rows into {table_name}")
            
        except Exception as e:
            logger.error(f"❌ Error loading {table_name}: {e}")


async def main():
    """Main initialization function"""
    
    logger.info("=" * 50)
    logger.info("COGNIX AI - Database Initialization")
    logger.info("=" * 50)
    
    logger.info("\n📊 Creating tables...")
    await create_tables()
    
    logger.info("\n📥 Loading CSV data...")
    await load_csv_data()
    
    logger.info("\n" + "=" * 50)
    logger.info("✅ Database initialization complete!")
    logger.info("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
