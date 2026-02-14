# ===============================
# ORACLE ENGINE
# Member 2 – Signal & Oracle Engineer
# ===============================
import numpy as np

# 1️⃣ Vibe Score Calculation
def calculate_vibe_score(daily_avg_sentiment):
    """
    Converts sentiment (-1 to +1)
    into 0–100 Vibe Score
    """

    if daily_avg_sentiment < -1 or daily_avg_sentiment > 1:
        raise ValueError("Sentiment must be between -1 and +1")

    vibe_score = (daily_avg_sentiment + 1) * 50
    return round(vibe_score, 2)



# 2️⃣ Sentiment Zone Classification
def classify_sentiment_zone(vibe_score):
    """
    Classifies vibe score into
    fear / neutral / greed
    """

    if vibe_score < 0 or vibe_score > 100:
        raise ValueError("Vibe score must be between 0 and 100")

    if vibe_score < 40:
        return "fear"
    elif vibe_score <= 60:
        return "neutral"
    else:
        return "greed"

def calculate_velocity(today_volume, yesterday_volume):
    """
    Calculates % change in tweet volume.
    """

    if yesterday_volume == 0:
        return 0.0

    velocity = ((today_volume - yesterday_volume) / yesterday_volume) * 100
    return round(velocity, 2)


def classify_velocity(velocity_value):
    """
    Classifies velocity into spike / stable / collapse
    """

    if velocity_value > 20:
        return "spike"
    elif velocity_value < -20:
        return "collapse"
    else:
        return "stable"

def calculate_correlation(sentiment_series, price_series):
    """
    Calculates correlation between sentiment and price trends.
    """

    if len(sentiment_series) != len(price_series):
        raise ValueError("Sentiment and price series must be same length")

    if len(sentiment_series) < 2:
        return 0.0

    correlation = np.corrcoef(sentiment_series, price_series)[0, 1]
    return round(float(correlation), 2)


def generate_contract_action(sentiment_zone, hype_velocity):
    """
    Simulates smart contract response.
    """

    if sentiment_zone == "greed" and hype_velocity == "spike":
        return "Increase liquidity incentives"

    if sentiment_zone == "fear" and hype_velocity == "collapse":
        return "Activate protection mode"

    if sentiment_zone == "neutral" and hype_velocity == "stable":
        return "Maintain protocol state"

    return "Monitor market conditions"



def determine_risk(sentiment_zone, hype_velocity, correlation_value):
    """
    Determines system risk level.
    """

    if sentiment_zone == "fear" and hype_velocity == "collapse":
        return "high"

    if abs(correlation_value) < 0.2:
        return "medium"

    return "low"



def calculate_oracle_confidence(vibe_score, velocity_value, correlation_value):
    """
    Combines signal strengths into confidence score (0–100).
    """

    sentiment_strength = abs(vibe_score - 50) * 2
    velocity_strength = min(abs(velocity_value), 100)
    correlation_strength = abs(correlation_value) * 100

    confidence = (sentiment_strength * 0.4 +
                  velocity_strength * 0.3 +
                  correlation_strength * 0.3)

    return round(min(confidence, 100), 2)


def build_oracle_output(daily_avg_sentiment,
                        today_volume,
                        yesterday_volume,
                        sentiment_series,
                        price_series):

    vibe_score = calculate_vibe_score(daily_avg_sentiment)
    sentiment_zone = classify_sentiment_zone(vibe_score)

    velocity_value = calculate_velocity(today_volume, yesterday_volume)
    hype_velocity = classify_velocity(velocity_value)

    correlation_value = calculate_correlation(sentiment_series, price_series)

    contract_action = generate_contract_action(sentiment_zone, hype_velocity)

    risk_level = determine_risk(sentiment_zone, hype_velocity, correlation_value)

    oracle_confidence = calculate_oracle_confidence(
        vibe_score,
        velocity_value,
        correlation_value
    )

    return {
        "vibe_score": vibe_score,
        "sentiment_zone": sentiment_zone,
        "hype_velocity": hype_velocity,
        "velocity_value": velocity_value,
        "correlation_value": correlation_value,
        "contract_action": contract_action,
        "risk_level": risk_level,
        "oracle_confidence": oracle_confidence
    }




import pandas as pd

def build_oracle_output_from_processed_csv(
    processed_csv_path="data/processed_sentiment.csv",
    price_series=None
):
    """
    Integration adapter:
    Reads Member 1 output CSV -> feeds your build_oracle_output().

    processed_csv contains: date, daily_avg_sentiment, daily_volume, ...
    (created by Member 1 sentiment_engine.py)
    """

    df = pd.read_csv(processed_csv_path)

    # Get ONE row per date (daily metrics)
    daily = df.groupby("date").agg(
        daily_avg_sentiment=("daily_avg_sentiment", "first"),
        daily_volume=("daily_volume", "first")
    ).reset_index()

    if len(daily) < 2:
        raise ValueError("Need at least 2 days of data to compute velocity.")

    # Sort by date
    daily = daily.sort_values("date")

    # Today & yesterday
    today = daily.iloc[-1]
    yesterday = daily.iloc[-2]

    daily_avg_sentiment = float(today["daily_avg_sentiment"])
    today_volume = int(today["daily_volume"])
    yesterday_volume = int(yesterday["daily_volume"])

    # Series for correlation (trend)
    sentiment_series = daily["daily_avg_sentiment"].astype(float).tolist()

    # If no price_series provided, use a simple placeholder (safe for demo)
    if price_series is None:
        # Placeholder: a steadily increasing series same length as sentiment_series
        price_series = list(range(1, len(sentiment_series) + 1))

    # Align lengths
    n = min(len(sentiment_series), len(price_series))
    sentiment_series = sentiment_series[-n:]
    price_series = price_series[-n:]

    return build_oracle_output(
        daily_avg_sentiment=daily_avg_sentiment,
        today_volume=today_volume,
        yesterday_volume=yesterday_volume,
        sentiment_series=sentiment_series,
        price_series=price_series
    )