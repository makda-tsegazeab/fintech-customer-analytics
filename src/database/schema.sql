# Save as: src/database/schema.sql
-- Task 3: PostgreSQL Database Schema for Bank Reviews
-- Database: bank_reviews

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS banks;

-- Create banks table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(bank_name)
);

-- Create reviews table
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score DECIMAL(5,4),
    source VARCHAR(50) DEFAULT 'Google Play Store',
    thumbs_up_count INTEGER DEFAULT 0,
    reviewer_name VARCHAR(100),
    app_version VARCHAR(20),
    scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
CREATE INDEX idx_reviews_sentiment ON reviews(sentiment_label);
CREATE INDEX idx_reviews_date ON reviews(review_date);

-- Create view for analysis
CREATE OR REPLACE VIEW bank_reviews_summary AS
SELECT 
    b.bank_name,
    COUNT(r.review_id) as total_reviews,
    AVG(r.rating) as avg_rating,
    ROUND(AVG(r.rating), 2) as avg_rating_rounded,
    COUNT(CASE WHEN r.sentiment_label = 'positive' THEN 1 END) as positive_count,
    COUNT(CASE WHEN r.sentiment_label = 'negative' THEN 1 END) as negative_count,
    COUNT(CASE WHEN r.sentiment_label = 'neutral' THEN 1 END) as neutral_count,
    MIN(r.review_date) as earliest_review,
    MAX(r.review_date) as latest_review
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_id, b.bank_name;

-- Create view for sentiment analysis
CREATE OR REPLACE VIEW sentiment_analysis AS
SELECT 
    b.bank_name,
    r.sentiment_label,
    COUNT(*) as review_count,
    ROUND(AVG(r.rating), 2) as avg_rating_for_sentiment,
    ROUND(AVG(r.sentiment_score), 3) as avg_sentiment_score
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
WHERE r.sentiment_label IS NOT NULL
GROUP BY b.bank_name, r.sentiment_label
ORDER BY b.bank_name, r.sentiment_label;

-- Create view for monthly trends
CREATE OR REPLACE VIEW monthly_trends AS
SELECT 
    b.bank_name,
    DATE_TRUNC('month', r.review_date) as review_month,
    COUNT(*) as monthly_reviews,
    AVG(r.rating) as avg_monthly_rating,
    COUNT(CASE WHEN r.sentiment_label = 'positive' THEN 1 END) as monthly_positive,
    COUNT(CASE WHEN r.sentiment_label = 'negative' THEN 1 END) as monthly_negative
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
WHERE r.review_date IS NOT NULL
GROUP BY b.bank_name, DATE_TRUNC('month', r.review_date)
ORDER BY b.bank_name, review_month;

-- Insert sample bank data (optional)
INSERT INTO banks (bank_name, app_name) VALUES
('Commercial Bank of Ethiopia', 'CBE Mobile Banking'),
('Bank of Abyssinia', 'BOA Mobile Banking'),
('Dashen Bank', 'Dashen Bank Mobile Banking')
ON CONFLICT (bank_name) DO NOTHING;