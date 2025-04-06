from fastapi import APIRouter, Query
from ..schemas.analyzer import AnalyzerResponse
from ..utils.analyzer import analyze_keyword_trends

analyzer = APIRouter()


@analyzer.get(
    "/analyze-keyword",
    summary="Google Treand Analyzer",
    description="This API allows you to analyze Google Trends data for specific keywords.",
    response_model=AnalyzerResponse,
)
def analyze_keyword_trends_endpoint(
    keyword: str = Query(
        description="Keyword to analyze.",
    ),
    timeframe: str = Query(
        "today 1-m",
        description=(
            "Timeframe for trend data. The accepted formats are:\n"
            "- Everything: 'all'\n"
            "- Specific dates: 'YYYY-MM-DD YYYY-MM-DD' (e.g., '2016-12-14 2017-01-25')\n"
            "- Specific datetimes: 'YYYY-MM-DDTHH YYYY-MM-DDTHH' (e.g., '2017-02-06T10 2017-02-12T07')\n"
            "- Time component is based on UTC.\n"
            "Current Time Minus Time Pattern:\n"
            "- By Month: 'today #-m' (valid for 1, 3, and 12 months only)\n"
            "- Daily: 'now #-d' (valid for 1, and 7 days only)\n"
            "- Hourly: 'now #-H' (valid for 1, and 4 hours only)\n"
        ),
    ),
    location: str = Query(
        description=(
            "Geo location for trend data. Accepted values are:\n"
            "- Two letter country abbreviation (e.g., 'US' for United States)\n"
            "- Defaults to 'WORLD' (global data)\n"
            "- More detail for States/Provinces by specifying additional abbreviations:\n"
            "    - 'US-AL' for Alabama\n"
            "    - 'GB-ENG' for England\n"
            "- Can also be a list of up to five regions, e.g. 'US,GB,DE,IN,CA'."
        ),
    ),
    trend_type: str = Query(
        description=(
            "What Google property to filter to. The accepted values are:\n"
            "- 'images': For image search trends.\n"
            "- 'news': For news search trends.\n"
            "- 'youtube': For YouTube search trends.\n"
            "- 'froogle': For Google Shopping results.\n"
            "Defaults to 'web' for web search trends. location must be empty to indicate web"
        ),
    ),
):
    return analyze_keyword_trends(keyword, timeframe, location, trend_type)
