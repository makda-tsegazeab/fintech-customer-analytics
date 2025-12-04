#!/usr/bin/env python3
"""
SQL queries to verify data integrity for Task 3
"""

import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def run_verification():
    """Run verification queries"""
    
    print("🔍 Running verification queries...")
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'bank_reviews'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )
        cursor = conn.cursor()
        
        print("✅ Connected to database")
        
        # Query 1: Total counts
        print("\n1. Total counts:")
        cursor.execute("SELECT COUNT(*) as total_banks FROM banks")
        print(f"   Banks: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) as total_reviews FROM reviews")
        print(f"   Reviews: {cursor.fetchone()[0]}")
        
        # Query 2: Reviews per bank
        print("\n2. Reviews per bank:")
        cursor.execute("""
            SELECT b.bank_name, COUNT(r.review_id) as review_count
            FROM banks b
            LEFT JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY review_count DESC
        """)
        
        for bank_name, count in cursor.fetchall():
            print(f"   {bank_name}: {count} reviews")
        
        # Query 3: Average rating per bank
        print("\n3. Average rating per bank:")
        cursor.execute("""
            SELECT b.bank_name, 
                   ROUND(AVG(r.rating), 2) as avg_rating,
                   MIN(r.rating) as min_rating,
                   MAX(r.rating) as max_rating
            FROM banks b
            JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY avg_rating DESC
        """)
        
        for bank_name, avg_rating, min_rating, max_rating in cursor.fetchall():
            print(f"   {bank_name}: {avg_rating} (range: {min_rating}-{max_rating})")
        
        # Query 4: Sentiment distribution
        print("\n4. Sentiment distribution:")
        cursor.execute("""
            SELECT b.bank_name, r.sentiment_label, COUNT(*) as count
            FROM reviews r
            JOIN banks b ON r.bank_id = b.bank_id
            WHERE r.sentiment_label IS NOT NULL
            GROUP BY b.bank_name, r.sentiment_label
            ORDER BY b.bank_name, r.sentiment_label
        """)
        
        current_bank = None
        for bank_name, sentiment, count in cursor.fetchall():
            if bank_name != current_bank:
                current_bank = bank_name
                print(f"   {bank_name}:")
            print(f"     {sentiment}: {count}")
        
        # Query 5: Date range of reviews
        print("\n5. Date range:")
        cursor.execute("""
            SELECT MIN(review_date) as earliest, MAX(review_date) as latest
            FROM reviews
            WHERE review_date IS NOT NULL
        """)
        
        earliest, latest = cursor.fetchone()
        print(f"   Earliest review: {earliest}")
        print(f"   Latest review: {latest}")
        
        # Query 6: Data quality check
        print("\n6. Data quality check:")
        
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE rating < 1 OR rating > 5")
        invalid_ratings = cursor.fetchone()[0]
        print(f"   Invalid ratings: {invalid_ratings}")
        
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE review_text IS NULL OR review_text = ''")
        empty_reviews = cursor.fetchone()[0]
        print(f"   Empty reviews: {empty_reviews}")
        
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE bank_id IS NULL")
        orphaned_reviews = cursor.fetchone()[0]
        print(f"   Orphaned reviews (no bank): {orphaned_reviews}")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Verification complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    run_verification()