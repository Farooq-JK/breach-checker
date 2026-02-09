# Handles communication with the Have I Been Pwned API

import requests
import time  # ✅ used for retry delay

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
        # ✅ try request twice max (retry once if rate limited)
        for attempt in range(4):

            response = requests.get(
                f"{BASE_URL}/breachedaccount/{email}",
                headers=headers,
                timeout=10
            )

            # ✅ breached
            if response.status_code == 200:
                breaches = response.json()
                sites = [b["Name"] for b in breaches]
                return True, sites

            # ✅ safe
            elif response.status_code == 404:
                return False, []

            # ✅ rate limit → wait then retry
            elif response.status_code == 429:
                print("Rate limited. Waiting before retry...")
                time.sleep(3)  # wait longer before retry
                continue  # try again

            # other unexpected codes
            else:
                print(f"API returned {response.status_code} for {email}")
                return False, []

        # if still failing after retry
        return False, []

    except requests.exceptions.RequestException as e:
        print(f"Connection error while checking {email}: {str(e)}")
        return False, []
