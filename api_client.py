import requests
import time
import logging

from config import API_KEY, BASE_URL

def check_email(email):
    return check_hibp(email)

# Provider 1: Have I Been Pwned (HIBP)
def check_hibp(email):

    headers = {
        "hibp-api-key": API_KEY,
        "user-agent": "breach-checker-app"
    }

    try:
        # retry a few times if rate limited
        for attempt in range(4):

            logging.info(f"HIBP request for {email} (attempt {attempt + 1})")

            response = requests.get(
                f"{BASE_URL}/breachedaccount/{email}",
                headers=headers,
                timeout=10
            )

            # breached
            if response.status_code == 200:
                breaches = response.json()
                sites = [b["Name"] for b in breaches]
                logging.info(f"Breaches found for {email}")
                return True, sites

            # safe
            elif response.status_code == 404:
                logging.info(f"No breaches found for {email}")
                return False, []

            # rate limited → retry
            elif response.status_code == 429:
                logging.warning("Rate limited (429). Waiting before retry...")
                time.sleep(3)
                continue

            # unexpected response
            else:
                logging.error(f"Unexpected API status {response.status_code} for {email}")
                return False, []

        logging.error(f"Max retries reached for {email}")
        return False, []

    except requests.exceptions.RequestException as e:
        logging.error(f"Connection error while checking {email}: {str(e)}")
        return False, []

