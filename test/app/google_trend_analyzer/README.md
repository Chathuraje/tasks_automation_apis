# 📈 Google Trends Keyword Analyzer API

Google Trend Analyzer API is a FastAPI-powered tool that analyzes any given keyword using Google Trends and tells you if it's **"worth targeting"** based on real-time trend data.

## ✅ Goal
Build a tool that:

1. Accepts a keyword or title (e.g. "Ethereum ETF approval").
2. Fetches relevant trend data via Google Trends.
3. Analyzes the trend (e.g. popularity over time, interest by region, related queries).
4. Determines keyword worthiness based on metrics like:
    - Consistency or spike in interest
    - Rising related keywords
    - Global vs local relevance
    - Seasonal pattern

## 🔧 Tools / Libraries
- Pytrends: An unofficial Google Trends API for Python.
- FastAPI: to expose this as an API.
- Scoring Logic: Create a custom scoring system (e.g. 0-100) based on volume, stability, relevance, etc.

## Explain the Scoring Logic



## 🚀 Features

- Analyze keyword popularity over the past given timeframe
- Get average & peak trend scores
- Discover top 5 related queries
- See where the keyword is trending globally
- Get a simple "worthiness" rating (High / Low)

## 🧠 Use Case

Perfect for:
- SEO experts
- YouTube creators
- Content strategists
- Marketers validating trending topics


## 🔍 Example
**Request**

```
GET /google-trend-analyzer/analyze?keyword=bitcoin halving&timeframe=today%201-m
```

## API accepts the following parameters:
- **Keyword**: A string representing the keyword to analyze.
- **Timeframe**: A string indicating the time period for the trend data, with the following accepted formats:
  - `Timeframe`: `Date to start from`
    - **Defaults** to last 5 years: `'today 5-y'`
    - **Everything**: `'all'`
    - **Specific dates**: `'YYYY-MM-DD YYYY-MM-DD'` (e.g. `'2016-12-14 2017-01-25'`)
    - **Specific datetimes**: `'YYYY-MM-DDTHH YYYY-MM-DDTHH'` (e.g. `'2017-02-06T10 2017-02-12T07'`)
    - **Note**: Time components are based on UTC.
  - **Current Time Minus Time Pattern**:
    - By Month: `'today #-m'` where `#` is the number of months to pull data for (valid for 1, 3, and 12 months only).
    - Daily: `'now #-d'` where `#` is the number of days to pull data for (valid for 1, and 7 days only).
    - Hourly: `'now #-H'` where `#` is the number of hours to pull data for (valid for 1, and 4 hours only).
- **location**: Specifies the location(s) for trend analysis. You can narrow down the trend data to specific countries, states, or regions.
  - **Two letter country abbreviation**: For example, `'US'` for the United States.
  - **Defaults to World**: If not provided, will use global data.
  - **More detailed information for States/Provinces**:
    - `'US-AL'` for Alabama
    - `'GB-ENG'` for England
  - **Can also be a list of up to five regions**:  
  For example: `'US,GB,DE,IN,CA'`
- **trend_type**: Specifies which Google property to filter the trend data by. This allows you to focus on trends from different Google services.
  - **Defaults to web searches**: If not provided, the data will be from web searches. (location must be empty to indicate web)
  - **Can be**:
    - `'images'`: For image search trends.
    - `'news'`: For news search trends.
    - `'youtube'`: For YouTube search trends.
    - `'froogle'`: For Google Shopping (froogle) results.

**Response**

```json
{
  "keyword": "bitcoin",
  "location": "US",
  "trend_type": "web",
  "composite_score": 83.7,
  "worthiness": "Very High",
  "components": {
    "average_trend_score": {
      "value": 73.0,
      "score": 29.2
    },
    "peak_trend_score": {
      "value": 100,
      "score": 10.0
    },
    "trend_stability": {
      "std_dev": 9.1,
      "score": 13.93
    },
    "rising_related_queries": {
      "found": true,
      "score": 20.0
    },
    "regional_interest": {
      "top_regions_above_50": 4,
      "score": 8.0,
      "top_5": {
        "United States": 78,
        "Canada": 65,
        "Germany": 58,
        "UK": 53,
        "India": 47
      }
    }
  },
  "related_queries_top_5": {
    "bitcoin news": "Breakout",
    "btc today": "Breakout",
    "bitcoin prediction": "Breakout"
  }
}
```

## 📌 Dependencies

- FastAPI
- PyTrends

## 🧠 Keyword Scoring System (0–100)

The system uses **5 measurable metrics** from Google Trends to assess the potential of a keyword. Each metric contributes a portion of the total 100 points.

### 1. 📊 Average Trend Score (0–40 points)

**What it means:**  
This is the **average popularity** of the keyword over the past 7 days on Google Trends (scale of 0 to 100).

- A higher average means the keyword is consistently searched.
- If a keyword scores **70 average**, you get:  
  `70 / 100 * 40 = 28 points`

✅ **Why it's important:**  
Consistency = sustained public interest. It’s a good sign for evergreen or currently active topics.

---

### 2. 🔥 Rising Related Queries (0–20 points)

**What it means:**  
Google Trends shows related search terms that are rapidly increasing in popularity (called “rising queries”).

- If the API returns **any rising terms**, the keyword gets full **20 points**.
- If there are **no rising terms**, it gets **0 points**.

✅ **Why it's important:**  
If people are searching not just the keyword but **variations and related terms**, it means there's momentum and depth in the trend.

---

### 3. 📈 Peak Score (0–10 points)

**What it means:**  
This captures the **maximum spike in popularity** in the last 7 days.

- If the keyword **reached 100**, it gets **10 points**.
- If it peaked at 60, you get:  
  `60 / 100 * 10 = 6 points`

✅ **Why it's important:**  
Sharp peaks can signal **events, news, or viral moments**. Good for capitalizing on trending or time-sensitive content.

---

### 4. 🌍 Regional Interest Strength (0–10 points)

**What it means:**  
We check the **top 5 countries or regions** where the keyword is searched.

- If **3 or more regions** show a score above 50, you get full **10 points**.
- If only 1 region is above 50, you get:  
  `1/5 * 10 = 2 points`

✅ **Why it's important:**  
Broad interest across multiple regions = higher opportunity for global content or international reach.

---

### 5. 📉 Trend Stability (0–20 points)

**What it means:**  
This measures how **volatile** the keyword is across the week using **standard deviation**.

- Low deviation = consistent trend = high score.
- High deviation = spiky, unpredictable = low score.

🔧 **How it's calculated:**  
- Max std deviation expected = 30  
- Score = `max(0, (1 - (std_dev / 30)) * 20)`

✅ **Why it's important:**  
Stable keywords are more **predictable and safe** for long-term content. Volatile trends may disappear quickly.

---

## 🧮 Total Score = Sum of All Metrics

| Metric                     | Max Points |
|----------------------------|------------|
| Average Trend Score        | 40         |
| Rising Related Queries     | 20         |
| Peak Score                 | 10         |
| Regional Interest          | 10         |
| Trend Stability            | 20         |
| **Total**                  | **100**    |

---

### 🏁 Final Worthiness Label

| Total Score | Worthiness |
|-------------|------------|
| 80–100      | 🔥 Very High (great to target) |
| 60–79       | ✅ High (solid opportunity)    |
| 40–59       | ⚠️ Medium (watch but validate) |
| < 40        | ❌ Low (likely not worth pursuing now) |

---

### 🧰 In Simple Terms

> “We don’t just check if people are Googling your keyword. We also see if it’s growing, where it's trending, how consistent it is, and what related topics are bubbling up — then we score it and tell you if it’s worth your time.”

## 📣 License

MIT License. Free to use and modify.