import os
import yaml
from dotenv import load_dotenv

# -------------------------------------------------
# Load environment variables (.env)
# -------------------------------------------------
load_dotenv()

# -------------------------------------------------
# Load YAML configuration file
# -------------------------------------------------
with open("config.yaml", "r", encoding="utf-8") as file:
    config_data = yaml.safe_load(file)

# -------------------------------------------------
# API Configuration (from config.yaml)
# -------------------------------------------------
BASE_URL = config_data["api"]["base_url"]
TIMEOUT = config_data["api"]["timeout"]
MAX_RETRIES = config_data["api"]["max_retries"]
RETRY_DELAY = config_data["api"]["retry_delay"]
POLITE_DELAY = config_data["api"]["polite_delay"]

# -------------------------------------------------
# Output Configuration
# -------------------------------------------------
SUMMARY_CHART = config_data["output"]["summary_chart"]

# -------------------------------------------------
# Secret API Key (from environment only)
# -------------------------------------------------
API_KEY = os.getenv("HIBP_API_KEY")
