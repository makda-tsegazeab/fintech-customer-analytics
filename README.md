# Customer Experience Analytics for Fintech Apps

## Project Overview
Analysis of customer satisfaction for three Ethiopian banking apps:
1. Commercial Bank of Ethiopia (CBE)
2. Bank of Abyssinia (BOA)
3. Dashen Bank

## Business Objective
Omega Consultancy is supporting banks to improve their mobile apps to enhance customer retention and satisfaction.

## Scenarios Analyzed
1. **Retaining Users**: Identify and address common issues affecting user retention
2. **Enhancing Features**: Extract desired features from user feedback
3. **Managing Complaints**: Cluster complaints to guide AI chatbot integration

## Project Structure

fintech-customer-analytics/
├── data/
│ ├── raw/ # Raw scraped data
│ ├── processed/ # Cleaned data
│ └── outputs/ # Analysis results
├── notebooks/ # Jupyter notebooks for exploration
├── src/
│ ├── scraping/ # Web scraping scripts
│ ├── analysis/ # NLP and sentiment analysis
│ ├── database/ # PostgreSQL setup and queries
│ └── visualization/ # Plotting scripts
├── tests/ # Unit tests
├── reports/ # Final report and visualizations
├── requirements.txt
├── .gitignore
└── README.md


## Installation
```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/fintech-customer-analytics.git

# Navigate to project
cd fintech-customer-analytics

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

Data Collection
Reviews are scraped from Google Play Store using google-play-scraper.

Methodology
Data Collection: Scrape 400+ reviews per bank (1200+ total)

Preprocessing: Clean, deduplicate, and normalize data

Sentiment Analysis: Classify reviews as Positive/Negative/Neutral

Thematic Analysis: Identify key themes and pain points

Database Storage: Store in PostgreSQL for persistence

Visualization: Create insights dashboards

Makda Tsegazeab Mammo


