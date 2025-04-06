import logging
from pytrends.request import TrendReq
import random
from ..config import CONFIG

# Access FastAPI's logger
logger = logging.getLogger("uvicorn")


# Format raw proxies to include username and password authentication
# Example: http://username:password@host:port
proxies = [
    f"http://{CONFIG.GTA_PROXY_USERNAME}:{CONFIG.GTA_PROXY_PASSWORD}@{ip}:{port}"
    for proxy in CONFIG.GTA_PROXY_HOST
    for ip, port in [proxy.split(":")]
]


def get_random_proxy():
    """
    Selects and returns one proxy randomly from the proxy pool.
    This helps distribute requests to avoid being blocked by Google Trends.
    """
    proxy = random.choice(proxies)
    logger.info(f"Selected Proxy: {proxy}")
    return proxy


def get_pytrends_instance(proxy):
    """
    Creates a Pytrends instance using the provided proxy.

    Args:
        proxy (str): Proxy URL (with auth) to use for the request.

    Returns:
        TrendReq: Configured pytrends instance.

    Raises:
        RuntimeError: If pytrends cannot be initialized with the proxy.
    """
    try:
        logger.info("Initializing pytrends instance.")
        return TrendReq(hl="en-US", tz=360, proxies=[proxy])
    except Exception as e:
        logger.error(f"Failed to initialize pytrends: {e}")
        raise RuntimeError(f"Failed to initialize pytrends: {e}")


def calculate_scores(trend_series):
    """
    Calculates performance metrics based on Google Trends time series data.

    Returns weighted scores:
        - Average trend score (importance: 40%)
        - Peak interest score (10%)
        - Stability score (inversely related to standard deviation, 20%)

    Args:
        trend_series (pandas.Series): Time-series trend data for a keyword.

    Returns:
        tuple: Raw values and their calculated weighted components.
    """
    avg_score = trend_series.mean()
    peak_score = trend_series.max()
    std_dev = trend_series.std()

    # Scoring weights applied to normalize each metric to a scale of 0–100
    avg_score_component = round((avg_score / 100) * 40, 2)
    peak_score_component = round((peak_score / 100) * 10, 2)
    stability_component = round(max(0, (1 - (std_dev / 30)) * 20), 2)

    logger.info(
        f"Calculated scores - Avg: {avg_score}, Peak: {peak_score}, Stability: {std_dev}"
    )
    return (
        avg_score,
        peak_score,
        std_dev,
        avg_score_component,
        peak_score_component,
        stability_component,
    )


def get_related_queries(pytrends, keyword):
    """
    Fetches rising related queries for the given keyword.

    Args:
        pytrends (TrendReq): Pytrends instance.
        keyword (str): The keyword being analyzed.

    Returns:
        tuple:
            - rising_terms (DataFrame or None): Rising search queries.
            - score (int): Related query score (20 if found, else 0).
    """
    try:
        logger.info(f"Fetching related queries for: {keyword}")
        related_data = pytrends.related_queries()
        related_queries = related_data.get(keyword, {})
        rising_terms = related_queries.get("rising")
        score = 20 if rising_terms is not None and not rising_terms.empty else 0
        logger.info(f"Related queries for {keyword}: {rising_terms}")
        return rising_terms, score
    except Exception as e:
        logger.error(f"Error fetching related queries for {keyword}: {e}")
        return None, 0


def get_regional_interest(pytrends, keyword):
    """
    Evaluates the regional popularity of the keyword.

    Returns a score based on how many regions have interest > 50
    and the top 5 regions by interest level.

    Args:
        pytrends (TrendReq): Pytrends instance.
        keyword (str): The keyword being analyzed.

    Returns:
        tuple: (strong region count, regional score, top 5 regions as dict)
    """
    try:
        logger.info(f"Fetching regional interest for: {keyword}")
        regional_interest = pytrends.interest_by_region()
        if not regional_interest.empty:
            top_regions = (
                regional_interest[keyword].sort_values(ascending=False).head(5)
            )
            strong_regions = sum(score > 50 for score in top_regions)
            region_score = round((strong_regions / 5) * 10, 2)
            top_5 = top_regions.to_dict()
            logger.info(f"Top regions for {keyword}: {top_5}")
        else:
            strong_regions = 0
            region_score = 0
            top_5 = {}
        return strong_regions, region_score, top_5
    except Exception as e:
        logger.error(f"Error fetching regional interest for {keyword}: {e}")
        return 0, 0, {}


def label_score(score):
    """
    Maps a numerical score to a human-readable category.

    Args:
        score (float): Composite trend score.

    Returns:
        str: Label such as 'Low', 'Medium', 'High', 'Very High'
    """
    if score >= 80:
        label = "Very High"
    elif score >= 60:
        label = "High"
    elif score >= 40:
        label = "Medium"
    else:
        label = "Low"

    logger.debug(f"Score label: {label}")
    return label


def analyze_keyword_trends(
    keyword: str, timeframe: str = "today 1-m", location: str = "", trend_type: str = ""
) -> dict:
    """
    Main function that analyzes the Google Trends performance of a keyword.

    Combines multiple dimensions such as:
        - Interest over time
        - Peak search volume
        - Search stability
        - Regional strength
        - Related rising queries

    Args:
        keyword (str): The keyword to analyze.
        timeframe (str): Date range (e.g., "today 1-m", "now 7-d").
        location (str): Country/region code (e.g., "US").
        trend_type (str): Type of search ('web', 'youtube', 'images', etc.).

    Returns:
        dict: Full trend analysis report including:
            - Scores
            - Related queries
            - Regional interest
            - Overall performance label
    """
    try:
        logger.info(
            f"Analyzing trends for keyword: {keyword}, Location: {location}, Trend Type: {trend_type}"
        )

        # Use proxy to avoid rate limits
        proxy = get_random_proxy()
        pytrends = get_pytrends_instance(proxy)

        # Load Google Trends data
        pytrends.build_payload(
            [keyword], timeframe=timeframe, geo=location, gprop=trend_type
        )
        interest_over_time = pytrends.interest_over_time()

        if interest_over_time.empty:
            logger.warning(f"No trend data found for keyword: {keyword}")
            return {"error": "No trend data found for this keyword."}

        # Analyze the time series data
        trend_series = interest_over_time[keyword]
        (
            avg,
            peak,
            std_dev,
            avg_score_component,
            peak_score_component,
            stability_component,
        ) = calculate_scores(trend_series)

        # Related queries score
        rising_terms, related_score = get_related_queries(pytrends, keyword)

        # Regional analysis
        strong_regions, region_score, regional_top5 = get_regional_interest(
            pytrends, keyword
        )

        # Final composite score out of 100
        total_score = round(
            avg_score_component
            + peak_score_component
            + stability_component
            + region_score,
            2,
        )
        worthiness = label_score(total_score)

        # Return structured analysis result
        result = {
            "keyword": keyword,
            "location": location,
            "trend_type": trend_type if trend_type else "web",
            "composite_score": total_score,
            "worthiness": worthiness,
            "components": {
                "average_trend_score": {
                    "value": round(avg, 2),
                    "score": avg_score_component,
                },
                "peak_trend_score": {
                    "value": int(peak),
                    "score": peak_score_component,
                },
                "trend_stability": {
                    "std_dev": round(std_dev, 2),
                    "score": stability_component,
                },
                "rising_related_queries": {
                    "found": rising_terms is not None and not rising_terms.empty,
                    "score": related_score,
                },
                "regional_interest": {
                    "top_regions_above_50": strong_regions,
                    "score": region_score,
                    "top_5": regional_top5,
                },
            },
            "related_queries_top_5": (
                rising_terms.head(5).to_dict() if rising_terms is not None else {}
            ),
        }

        logger.info(f"Trend analysis for {keyword} completed successfully.")
        return result

    except Exception as e:
        logger.error(f"Error occurred while analyzing keyword {keyword}: {e}")
        return {"error": f"Something went wrong while analyzing trends: {str(e)}"}
