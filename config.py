# Loads API settings (like API key) from the .env file

import os
from dotenv import load_dotenv

# Read variables from .env into environment
load_dotenv()

# Get API key safely from environment (not hardcoded)
API_KEY = os.getenv("HIBP_API_KEY")

# Base URL for the Have I Been Pwned API
BASE_URL = "https://haveibeenpwned.com/api/v3"
