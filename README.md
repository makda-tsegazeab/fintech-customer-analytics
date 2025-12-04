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

## Task 1: Data Collection and Preprocessing

### Methodology
1. **App Identification**: Used Google Play Store to identify official banking apps:
   - Commercial Bank of Ethiopia: `com.combanketh.mobilebanking`
   - Bank of Abyssinia: `com.bankofabyssinia.boa`
   - Dashen Bank: `com.dashenmobile`

2. **Web Scraping**: Used `google-play-scraper` Python library to collect:
   - Review text
   - Star ratings (1-5)
   - Posting dates
   - App name and source

3. **Target Volume**: Collected 400+ reviews per bank, exceeding the 1200 total requirement.

4. **Data Cleaning**:
   - Removed duplicate reviews
   - Handled missing values
   - Normalized dates to YYYY-MM-DD format
   - Validated ratings (1-5 range only)

5. **Output**: Saved as CSV with columns: `review`, `rating`, `date`, `bank`, `source`

### Results
- Total reviews collected: [INSERT NUMBER]
- Data quality: <5% missing values ✅
- Requirements met: 400+ per bank, 1200+ total ✅

### Files Created
- `data/reviews.csv`: Cleaned review data
- `src/scraping/task1_scrape.py`: Main scraping script
- `src/scraping/task1_preprocess.py`: Data quality check script



## Task 2: Sentiment and Thematic Analysis

### Methodology
1. **Sentiment Analysis**:
   - Used `distilbert-base-uncased-finetuned-sst-2-english` model via HuggingFace Transformers
   - Classified reviews as Positive/Negative/Neutral with confidence scores
   - Aggregated results by bank and rating

2. **Thematic Analysis**:
   - **Keyword Extraction**: Used TF-IDF and spaCy to extract significant keywords
   - **Theme Clustering**: Manually grouped keywords into 3-5 themes per bank:
     - Login & Security Issues
     - Transaction Problems  
     - App Performance & Bugs
     - User Interface & Experience
     - Customer Support
     - Feature Requests
   - **Theme Assignment**: Mapped reviews to themes based on keyword presence

### Results
- **Sentiment Analysis Complete**: 100% of reviews analyzed ✅
- **Themes Identified**: 3+ themes per bank ✅
- **Key Findings**:
  - Commercial Bank of Ethiopia: High positive sentiment (matching 4.2 rating)
  - Bank of Abyssinia: More negative sentiment around transaction issues
  - Dashen Bank: Balanced sentiment with UI/UX as strong point

### Files Created
- `data/outputs/reviews_with_sentiment.csv`: Reviews with sentiment labels
- `data/outputs/sentiment_summary.json`: Sentiment statistics
- `data/outputs/thematic_analysis.json`: Theme analysis results
- `data/outputs/bank_themes_summary.csv`: Theme distribution by bank
- `data/outputs/insights_recommendations.csv`: Business insights

### Visualizations
- Sentiment distribution pie charts
- Rating vs sentiment bar charts
- Theme comparison across banks
- Word clouds for each bank

### Requirements Met
- ✓ Sentiment scores for 90%+ reviews (100% achieved)
- ✓ 3+ themes per bank identified
- ✓ Modular pipeline code
- ✓ Minimum essential: Sentiment for 400+ reviews, 2+ themes per bank

## Task 3: PostgreSQL Database

**Database**: `bank_reviews`

**Tables**:
```sql
-- banks table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(100)
);

-- reviews table  
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score DECIMAL(5,4),
    source VARCHAR(50) DEFAULT 'Google Play Store'
);