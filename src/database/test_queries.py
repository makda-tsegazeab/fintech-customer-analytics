# Save as: src/database/test_queries.py
"""
Test SQL queries to verify database functionality
"""

from db_connection import DatabaseManager

def test_database():
    """Run test queries to verify database setup"""
    
    print("🧪 Testing Database Queries")
    print("="*60)
    
    db = DatabaseManager()
    
    if not db.connect():
        print("❌ Cannot connect to database")
        return False
    
    try:
        # Test 1: List all banks
        print("\n1. List all banks:")
        banks = db.execute_query("SELECT * FROM banks ORDER BY bank_id;", fetch=True)
        for bank in banks:
            print(f"   {bank['bank_id']}. {bank['bank_name']} - {bank['app_name']}")
        
        # Test 2: Count reviews
        print("\n2. Review statistics:")
        stats = db.execute_query("SELECT * FROM bank_reviews_summary;", fetch=True)
        for stat in stats:
            print(f"   {stat['bank_name']}:")
            print(f"     Total Reviews: {stat['total_reviews'] or 0}")
            print(f"     Avg Rating: {stat['avg_rating_rounded'] or 'N/A'}")
            if stat['positive_count']:
                print(f"     Positive: {stat['positive_count']}")
            if stat['negative_count']:
                print(f"     Negative: {stat['negative_count']}")
        
        # Test 3: Sentiment analysis
        print("\n3. Sentiment analysis:")
        sentiment = db.execute_query("SELECT * FROM sentiment_analysis;", fetch=True)
        for s in sentiment:
            print(f"   {s['bank_name']} - {s['sentiment_label']}:")
            print(f"     Reviews: {s['review_count']}, Avg Score: {s['avg_sentiment_score']}")
        
        # Test 4: Sample reviews
        print("\n4. Sample reviews:")
        reviews = db.execute_query("""
            SELECT b.bank_name, r.review_text, r.rating, r.sentiment_label
            FROM reviews r
            JOIN banks b ON r.bank_id = b.bank_id
            LIMIT 3;
        """, fetch=True)
        
        for i, review in enumerate(reviews, 1):
            print(f"   {i}. [{review['bank_name']}] Rating: {review['rating']}, Sentiment: {review['sentiment_label']}")
            print(f"      Review: {review['review_text'][:80]}...")
        
        # Test 5: Advanced query - Find common complaints
        print("\n5. Common negative keywords:")
        complaints = db.execute_query("""
            SELECT 
                b.bank_name,
                COUNT(*) as complaint_count,
                STRING_AGG(DISTINCT 
                    CASE 
                        WHEN LOWER(r.review_text) LIKE '%crash%' THEN 'crash'
                        WHEN LOWER(r.review_text) LIKE '%slow%' THEN 'slow'
                        WHEN LOWER(r.review_text) LIKE '%error%' THEN 'error'
                        WHEN LOWER(r.review_text) LIKE '%login%' THEN 'login'
                        WHEN LOWER(r.review_text) LIKE '%transfer%' THEN 'transfer'
                    END, ', ') as issue_types
            FROM reviews r
            JOIN banks b ON r.bank_id = b.bank_id
            WHERE r.sentiment_label = 'negative'
            AND (
                LOWER(r.review_text) LIKE '%crash%'
                OR LOWER(r.review_text) LIKE '%slow%'
                OR LOWER(r.review_text) LIKE '%error%'
                OR LOWER(r.review_text) LIKE '%login%'
                OR LOWER(r.review_text) LIKE '%transfer%'
            )
            GROUP BY b.bank_name
            ORDER BY complaint_count DESC;
        """, fetch=True)
        
        for complaint in complaints:
            if complaint['issue_types']:
                print(f"   {complaint['bank_name']}: {complaint['complaint_count']} complaints")
                print(f"      Issues: {complaint['issue_types']}")
        
        print("\n✅ All test queries executed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    finally:
        db.disconnect()

if __name__ == "__main__":
    success = test_database()
    if success:
        print("\n" + "="*60)
        print("🎉 DATABASE TEST PASSED - Ready for Task 4!")
        print("="*60)
    else:
        print("\n⚠️  Database test failed. Please check your setup.")