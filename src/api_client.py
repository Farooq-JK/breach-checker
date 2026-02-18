import requests
import time
import logging

from src.config import API_KEY, BASE_URL, TIMEOUT, MAX_RETRIES, RETRY_DELAY


# -------------------------------------------------
# Public function used by main.py
# DO NOT change this signature
# Allows swapping/adding providers internally
# -------------------------------------------------

def check_email(email):
    return check_hibp(email)

# Provider 1: Have I Been Pwned (HIBP)
# -------------------------------------------------

def check_hibp(email):

    headers = {
        "hibp-api-key": API_KEY,
        "user-agent": "breach-checker-app"
    }

    try:
        # Retry based on config value (not hardcoded)
        for attempt in range(MAX_RETRIES):

            logging.info(f"HIBP request for {email} (attempt {attempt + 1})")

            response = requests.get(
                f"{BASE_URL}/breachedaccount/{email}",
                headers=headers,
                timeout=TIMEOUT  # Now uses YAML config
            )

            # 200 → Breached
            if response.status_code == 200:
                breaches = response.json()
                sites = [b["Name"] for b in breaches]
                logging.info(f"Breaches found for {email}")
                return True, sites

            # 404 → Safe
            elif response.status_code == 404:
                logging.info(f"No breaches found for {email}")
                return False, []

            # 429 → Rate limited (retry)
            elif response.status_code == 429:
                logging.warning("Rate limited (429). Waiting before retry...")
                time.sleep(RETRY_DELAY)  # Now from config
                continue

            # Unexpected response
            else:
                logging.error(f"Unexpected API status {response.status_code} for {email}")
                return False, []

        # If max retries reached
        logging.error(f"Max retries reached for {email}")
        return False, []

    except requests.exceptions.RequestException as e:
        logging.error(f"Connection error while checking {email}: {str(e)}")
        return False, []
