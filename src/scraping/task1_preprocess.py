# Save as: src/scraping/task1_preprocess.py
"""
Additional preprocessing as needed
"""

import pandas as pd

def check_data_quality():
    """Check if data meets Task 1 requirements"""
    
    try:
        df = pd.read_csv('../../data/raw/reviews.csv')
        
        print("="*60)
        print("DATA QUALITY CHECK - TASK 1")
        print("="*60)
        
        # 1. Total reviews
        print(f"Total reviews: {len(df)}")
        print(f"Required: 1200+")
        print(f"Status: {'✅' if len(df) >= 1200 else '❌'}")
        
        # 2. Reviews per bank
        print("\nReviews per bank (need 400+ each):")
        for bank in df['bank'].unique():
            count = len(df[df['bank'] == bank])
            status = "✅" if count >= 400 else "❌"
            print(f"  {status} {bank}: {count}")
        
        # 3. Columns check
        required_cols = ['review', 'rating', 'date', 'bank', 'source']
        missing_cols = [col for col in required_cols if col not in df.columns]
        print(f"\nRequired columns: {required_cols}")
        print(f"Missing columns: {missing_cols if missing_cols else 'None ✅'}")
        
        # 4. Missing data
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        print(f"\nMissing data: {missing_pct:.2f}%")
        print(f"Target: <5%")
        print(f"Status: {'✅' if missing_pct < 5 else '❌'}")
        
        # 5. Date format
        try:
            pd.to_datetime(df['date'])
            print(f"\nDate format: Valid ✅")
        except:
            print(f"\nDate format: Invalid ❌")
        
        # 6. Rating range
        valid_ratings = df['rating'].between(1, 5).all()
        print(f"\nRatings valid (1-5): {'✅' if valid_ratings else '❌'}")
        
        return len(df) >= 1200
        
    except FileNotFoundError:
        print("❌ data/reviews.csv not found")
        return False

if __name__ == "__main__":
    check_data_quality()