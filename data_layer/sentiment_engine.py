import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

print("🚀 Starting Sentiment Engine...")

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# =========================
# 1. LOAD DATA
# =========================

df = pd.read_csv("data/twitter_dataset.csv")

print("Original Columns:", df.columns.tolist())
print("Original Rows:", len(df))

# Rename columns properly
df.rename(columns={
    "Text": "tweet_text",
    "Timestamp": "date"
}, inplace=True)

# =========================
# 2. DATA CLEANING
# =========================

# Remove duplicates
df = df.drop_duplicates()

# Remove empty tweets
df = df.dropna(subset=["tweet_text"])

# Remove URLs
df["tweet_text"] = df["tweet_text"].apply(
    lambda x: re.sub(r"http\S+", "", str(x))
)

# Convert date to YYYY-MM-DD
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

print("Rows after cleaning:", len(df))

# =========================
# 3. SENTIMENT ANALYSIS
# =========================

def analyze_sentiment(text):
    score = analyzer.polarity_scores(str(text))["compound"]

    if score > 0.05:
        label = "positive"
    elif score < -0.05:
        label = "negative"
    else:
        label = "neutral"

    return pd.Series([score, label])

df[["sentiment_score", "sentiment_label"]] = df["tweet_text"].apply(analyze_sentiment)

print("Sentiment scoring complete")

# =========================
# 4. DAILY AGGREGATION
# =========================

daily_stats = df.groupby("date").agg(
    daily_avg_sentiment=("sentiment_score", "mean"),
    daily_volume=("tweet_text", "count")
).reset_index()

# Calculate momentum
daily_stats["sentiment_momentum"] = daily_stats["daily_avg_sentiment"].diff().fillna(0)

# Merge back to main dataframe
df = df.merge(daily_stats, on="date", how="left")

# =========================
# 5. FINAL STRICT FORMAT
# =========================

df = df[[
    "date",
    "tweet_text",
    "sentiment_score",
    "sentiment_label",
    "daily_avg_sentiment",
    "daily_volume",
    "sentiment_momentum"
]]

# Ensure correct data types
df["date"] = df["date"].astype(str)
df["sentiment_score"] = df["sentiment_score"].astype(float)
df["daily_avg_sentiment"] = df["daily_avg_sentiment"].astype(float)
df["daily_volume"] = df["daily_volume"].astype(int)
df["sentiment_momentum"] = df["sentiment_momentum"].astype(float)

# =========================
# 6. SAVE OUTPUT
# =========================

df.to_csv("data/processed_sentiment.csv", index=False)

print("✅ SUCCESS — processed_sentiment.csv created.")
print(df.head())
# ==============TESTING===============
print("\nFinal Columns:")
print(df.columns.tolist())
print("\nMin Sentiment:", df["sentiment_score"].min())
print("Max Sentiment:", df["sentiment_score"].max())
daily = df.groupby("date")["daily_avg_sentiment"].first()
print("\nDaily averages sample:")
print(daily.head(5))
# Find most positive day
max_day = df.loc[df["daily_avg_sentiment"].idxmax()]
print("\nMost Positive Day:")
print(max_day[["date", "daily_avg_sentiment", "sentiment_momentum"]])

# Find most negative day
min_day = df.loc[df["daily_avg_sentiment"].idxmin()]
print("\nMost Negative Day:")
print(min_day[["date", "daily_avg_sentiment", "sentiment_momentum"]])
