from typing import Dict, Optional
from pydantic import BaseModel


class ScoreComponent(BaseModel):
    value: Optional[float] = None
    score: float


class TrendStability(BaseModel):
    std_dev: float
    score: float


class RisingRelatedQueries(BaseModel):
    found: bool
    score: float


class RegionalInterest(BaseModel):
    top_regions_above_50: int
    score: float
    top_5: Dict[str, int]


class AnalyzerComponents(BaseModel):
    average_trend_score: ScoreComponent
    peak_trend_score: ScoreComponent
    trend_stability: TrendStability
    rising_related_queries: RisingRelatedQueries
    regional_interest: RegionalInterest


class AnalyzerResponse(BaseModel):
    keyword: str
    location: str
    trend_type: str
    composite_score: float
    worthiness: str
    components: AnalyzerComponents
    related_queries_top_5: Dict[str, str]

    class Config:
        json_schema_extra = {
            "example": {
                "keyword": "bitcoin",
                "location": "US",
                "trend_type": "web",
                "composite_score": 83.7,
                "worthiness": "Very High",
                "components": {
                    "average_trend_score": {"value": 73.0, "score": 29.2},
                    "peak_trend_score": {"value": 100.0, "score": 10.0},
                    "trend_stability": {"std_dev": 9.1, "score": 13.93},
                    "rising_related_queries": {"found": True, "score": 20.0},
                    "regional_interest": {
                        "top_regions_above_50": 4,
                        "score": 8.0,
                        "top_5": {
                            "United States": 78,
                            "Canada": 65,
                            "Germany": 58,
                            "UK": 53,
                            "India": 47,
                        },
                    },
                },
                "related_queries_top_5": {
                    "bitcoin news": "Breakout",
                    "btc today": "Breakout",
                    "bitcoin prediction": "Breakout",
                },
            }
        }
