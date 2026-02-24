import os
import yaml
from dotenv import load_dotenv

# Load environment variables from the .env file
# This is where sensitive values like API keys are stored
load_dotenv()

# Read settings from the external config.yaml file
# This allows changing system behaviour without editing the code
with open("config.yaml", "r", encoding="utf-8") as file:
    config_data = yaml.safe_load(file)

# API-related settings taken from config.yaml
BASE_URL = config_data["api"]["base_url"]    
TIMEOUT = config_data["api"]["timeout"]       
MAX_RETRIES = config_data["api"]["max_retries"]  
RETRY_DELAY = config_data["api"]["retry_delay"]  
POLITE_DELAY = config_data["api"]["polite_delay"]  

# Output settings (e.g., whether to generate a summary chart)
SUMMARY_CHART = config_data["output"]["summary_chart"]

# Load the secret API key from environment variables only
# This keeps it out of the source code for security reasons
API_KEY = os.getenv("HIBP_API_KEY")