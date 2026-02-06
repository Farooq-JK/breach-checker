# config.py
# Loads API settings from environment variables

import os
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()

# HIBP key
API_KEY = os.getenv("HIBP_API_KEY")

# HIBP base endpoint
BASE_URL = "https://haveibeenpwned.com/api/v3"
