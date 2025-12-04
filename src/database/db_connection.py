# Save as: src/database/db_connection.py
"""
PostgreSQL Database Connection Utilities for Task 3
"""

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import pandas as pd
import os
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

class DatabaseManager:
    """Manage PostgreSQL database operations"""
    
    def __init__(self, dbname=None, user=None, password=None, host=None, port=None):
        """Initialize database connection parameters"""
        self.dbname = dbname or os.getenv('DB_NAME', 'bank_reviews')
        self.user = user or os.getenv('DB_USER', 'postgres')
        self.password = password or os.getenv('DB_PASSWORD', '')
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.port = port or os.getenv('DB_PORT', '5432')
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print(f"✅ Connected to database: {self.dbname}")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute SQL query"""
        try:
            self.cursor.execute(query, params or ())
            if fetch:
                return self.cursor.fetchall()
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"❌ Query execution failed: {e}")
            return False
    
    def create_tables(self):
        """Create database tables from schema.sql"""
        try:
            # Read schema file
            schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            # Execute schema
            self.cursor.execute(schema_sql)
            self.connection.commit()
            print("✅ Database tables created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
            return False
    
    def insert_bank(self, bank_name, app_name):
        """Insert a bank record"""
        query = """
        INSERT INTO banks (bank_name, app_name) 
        VALUES (%s, %s)
        ON CONFLICT (bank_name) DO NOTHING
        RETURNING bank_id;
        """
        result = self.execute_query(query, (bank_name, app_name), fetch=True)
        if result:
            return result[0]['bank_id'] if result else None
        return None
    
    def insert_review(self, review_data):
        """Insert a review record"""
        query = """
        INSERT INTO reviews (
            bank_id, review_text, rating, review_date, 
            sentiment_label, sentiment_score, source,
            thumbs_up_count, reviewer_name, app_version
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING review_id;
        """
        params = (
            review_data.get('bank_id'),
            review_data.get('review_text'),
            review_data.get('rating'),
            review_data.get('review_date'),
            review_data.get('sentiment_label'),
            review_data.get('sentiment_score'),
            review_data.get('source', 'Google Play Store'),
            review_data.get('thumbs_up_count', 0),
            review_data.get('reviewer_name'),
            review_data.get('app_version')
        )
        result = self.execute_query(query, params, fetch=True)
        if result:
            return result[0]['review_id']
        return None
    
    def get_bank_id(self, bank_name):
        """Get bank_id by bank name"""
        query = "SELECT bank_id FROM banks WHERE bank_name = %s;"
        result = self.execute_query(query, (bank_name,), fetch=True)
        return result[0]['bank_id'] if result else None
    
    def load_reviews_from_csv(self, csv_path):
        """Load reviews from CSV file into database"""
        try:
            # Read CSV file
            df = pd.read_csv(csv_path)
            print(f"📊 Loading {len(df)} reviews from {csv_path}")
            
            inserted_count = 0
            skipped_count = 0
            
            for _, row in df.iterrows():
                # Get or create bank
                bank_name = row.get('bank')
                if not bank_name:
                    skipped_count += 1
                    continue
                
                bank_id = self.get_bank_id(bank_name)
                if not bank_id:
                    # Insert new bank
                    bank_id = self.insert_bank(bank_name, f"{bank_name} Mobile Banking")
                
                # Prepare review data
                review_data = {
                    'bank_id': bank_id,
                    'review_text': row.get('review', ''),
                    'rating': int(row.get('rating', 0)),
                    'review_date': row.get('date'),
                    'sentiment_label': row.get('sentiment_label'),
                    'sentiment_score': float(row.get('sentiment_score', 0.5)) if pd.notna(row.get('sentiment_score')) else 0.5,
                    'source': row.get('source', 'Google Play Store'),
                    'thumbs_up_count': row.get('thumbs_up', 0) if 'thumbs_up' in row else 0,
                    'reviewer_name': row.get('reviewer_name', 'Anonymous'),
                    'app_version': row.get('app_version', 'Unknown')
                }
                
                # Insert review
                if self.insert_review(review_data):
                    inserted_count += 1
                else:
                    skipped_count += 1
                
                # Progress indicator
                if inserted_count % 100 == 0:
                    print(f"  Processed {inserted_count} reviews...")
            
            print(f"✅ Data loading complete: {inserted_count} inserted, {skipped_count} skipped")
            return inserted_count
            
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            return 0
    
    def get_summary_statistics(self):
        """Get summary statistics from database"""
        query = """
        SELECT 
            (SELECT COUNT(*) FROM banks) as total_banks,
            (SELECT COUNT(*) FROM reviews) as total_reviews,
            (SELECT AVG(rating) FROM reviews) as overall_avg_rating,
            (SELECT COUNT(DISTINCT bank_id) FROM reviews) as banks_with_reviews;
        """
        return self.execute_query(query, fetch=True)
    
    def export_to_csv(self, output_path):
        """Export all reviews to CSV"""
        try:
            query = """
            SELECT 
                b.bank_name,
                r.review_text,
                r.rating,
                r.review_date,
                r.sentiment_label,
                r.sentiment_score,
                r.source,
                r.created_at
            FROM reviews r
            JOIN banks b ON r.bank_id = b.bank_id
            ORDER BY r.review_date DESC;
            """
            
            df = pd.read_sql_query(query, self.connection)
            df.to_csv(output_path, index=False)
            print(f"✅ Data exported to {output_path} ({len(df)} records)")
            return output_path
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return None

# Helper function for quick setup
def setup_database():
    """Quick setup function for Task 3"""
    print("="*60)
    print("TASK 3: POSTGRESQL DATABASE SETUP")
    print("="*60)
    
    # Create database manager
    db = DatabaseManager()
    
    if not db.connect():
        print("\n⚠️  Connection failed. Please check:")
        print("   1. PostgreSQL service is running")
        print("   2. Database 'bank_reviews' exists")
        print("   3. Correct credentials in .env file")
        return False
    
    # Create tables
    print("\n📋 Creating database tables...")
    if not db.create_tables():
        print("⚠️  Table creation failed. They might already exist.")
    
    # Load data if available
    print("\n📥 Loading data into database...")
    
    # Try different CSV paths
    csv_paths = [
        '../../data/outputs/reviews_with_sentiment.csv',
        '../data/outputs/reviews_with_sentiment.csv',
        'data/outputs/reviews_with_sentiment.csv',
        '../../data/raw/reviews.csv'
    ]
    
    data_loaded = False
    for csv_path in csv_paths:
        if os.path.exists(csv_path):
            print(f"Found data file: {csv_path}")
            inserted = db.load_reviews_from_csv(csv_path)
            if inserted > 0:
                data_loaded = True
                break
    
    if not data_loaded:
        print("⚠️  No data files found. Creating sample data...")
        # Create minimal sample data
        db.insert_bank('Commercial Bank of Ethiopia', 'CBE Mobile Banking')
        db.insert_bank('Bank of Abyssinia', 'BOA Mobile Banking')
        db.insert_bank('Dashen Bank', 'Dashen Bank Mobile Banking')
        print("✅ Created sample bank records")
    
    # Get summary
    print("\n📊 Database Summary:")
    summary = db.get_summary_statistics()
    if summary:
        for key, value in summary[0].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Export to CSV for verification
    print("\n💾 Exporting data for verification...")
    export_path = 'data/outputs/database_export.csv'
    db.export_to_csv(export_path)
    
    # Close connection
    db.disconnect()
    
    print("\n" + "="*60)
    print("✅ TASK 3 DATABASE SETUP COMPLETE")
    print("="*60)
    
    return True

if __name__ == "__main__":
    setup_database()