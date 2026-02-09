# Handles communication with the Have I Been Pwned API

import requests
import time
import logging  # ✅ professional logging

from config import API_KEY, BASE_URL


def check_email(email):
    """
    Check one email against the API.

    Returns:
        (True, [breach names])  -> if breached
        (False, [])            -> if safe
    """

    headers = {
        "hibp-api-key": API_KEY,
        "user-agent": "breach-checker-app"
    }

    try:
        # ✅ retry a few times if rate limited
        for attempt in range(4):

            logging.info(f"Sending request for {email} (attempt {attempt + 1})")

            response = requests.get(
                f"{BASE_URL}/breachedaccount/{email}",
                headers=headers,
                timeout=10  # prevents hanging forever
            )

            # ✅ breached
            if response.status_code == 200:
                breaches = response.json()
                sites = [b["Name"] for b in breaches]
                logging.info(f"Breaches found for {email}")
                return True, sites

            # ✅ safe
            elif response.status_code == 404:
                logging.info(f"No breaches found for {email}")
                return False, []

            # ✅ rate limit → wait and retry
            elif response.status_code == 429:
                logging.warning("Rate limited (429). Waiting before retry...")
                time.sleep(3)
                continue

            # ❌ unexpected status
            else:
                logging.error(f"Unexpected API status {response.status_code} for {email}")
                return False, []

        # ❌ still failing after retries
        logging.error(f"Max retries reached for {email}")
        return False, []

    # ❌ network problems
    except requests.exceptions.RequestException as e:
        logging.error(f"Connection error while checking {email}: {str(e)}")
        return False, []
