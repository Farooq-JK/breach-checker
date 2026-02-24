import requests
import time
import logging

from src.config import API_KEY, BASE_URL, TIMEOUT, MAX_RETRIES, RETRY_DELAY


# This is the function used by main.py.
# If we ever change the provider, we only update it here.
def check_email(email):
    return check_hibp(email)


# Checks an email address using the Have I Been Pwned API
def check_hibp(email):

    # Set up the required headers (API key + app name)
    headers = {
        "hibp-api-key": API_KEY,
        "user-agent": "breach-checker-app"
    }

    try:
        # Try the request several times in case of temporary issues
        for attempt in range(MAX_RETRIES):

            logging.info(f"Checking {email} (attempt {attempt + 1})")

            # Send request to the HIBP endpoint
            response = requests.get(
                f"{BASE_URL}/breachedaccount/{email}",
                headers=headers,
                timeout=TIMEOUT
            )

            # If we get 200, the email was found in one or more breaches
            if response.status_code == 200:
                breaches = response.json()
                sites = [b["Name"] for b in breaches]  # Get breach names only
                logging.info(f"Breaches found for {email}")
                return True, sites

            # 404 means the email was not found (good news)
            elif response.status_code == 404:
                logging.info(f"No breaches found for {email}")
                return False, []

            # 429 means we hit the rate limit, so wait and try again
            elif response.status_code == 429:
                logging.warning("Rate limit reached. Waiting before retrying...")
                time.sleep(RETRY_DELAY)
                continue

            # Any other response is unexpected, so we log it and stop
            else:
                logging.error(f"Unexpected status {response.status_code} for {email}")
                return False, []

        # If all retries are used, we stop trying
        logging.error(f"Stopped checking {email} after maximum retries")
        return False, []

    # Catch connection or network errors
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error while checking {email}: {str(e)}")
        return False, []