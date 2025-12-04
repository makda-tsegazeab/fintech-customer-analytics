# Save as: src/scraping/find_apps.py
from google_play_scraper import search

banks = [
    "Commercial Bank of Ethiopia",
    "Bank of Abyssinia", 
    "Dashen Bank"
]

for bank in banks:
    print(f"\n🔍 Searching for: {bank}")
    results = search(f"{bank} mobile banking", n_hits=3)
    
    if results:
        for i, app in enumerate(results):
            print(f"{i+1}. {app['title']}")
            print(f"   App ID: {app['appId']}")
            print(f"   Developer: {app.get('developer', 'N/A')}")
            print(f"   Rating: {app.get('score', 'N/A')}")
            print(f"   Installs: {app.get('installs', 'N/A')}")
            print()
    else:
        print("   No results found")