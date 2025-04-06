import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Configuration settings for the Google Trend Analyzer
class CONFIG:
    GTA_PROXY_USERNAME = os.getenv("GTA_PROXY_USERNAME")
    GTA_PROXY_PASSWORD = os.getenv("GTA_PROXY_PASSWORD")

    # Raw proxy IPs (host:port) for rotating requests to avoid Google rate limits.
    # These are used with authentication to create full proxy URLs.
    GTA_PROXY_HOST = [
        "38.153.152.244:9594",
        "86.38.234.176:6630",
        "173.211.0.148:6641",
        "161.123.152.115:6360",
        "216.10.27.159:6837",
        "154.36.110.199:6853",
        "45.151.162.198:6600",
        "185.199.229.156:7492",
        "185.199.228.220:7300",
        "185.199.231.45:8382",
    ]


config = CONFIG()
