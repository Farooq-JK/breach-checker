# api_client.py
# Handles communication with the Have I Been Pwned API

import requests
from config import API_KEY, BASE_URL


def check_email(email):
    """
    Returns:
        (True, [breach names])  -> if breached
        (False, [])            -> if safe
    """

    headers = {
        # HIBP requires this exact header name
        "hibp-api-key": API_KEY,
        "user-agent": "breach-checker-app"   # required by HIBP
    }

    try:
        # HIBP uses GET not POST
        response = requests.get(
            f"{BASE_URL}/breachedaccount/{email}",
            headers=headers,
            timeout=10
        )

        # 200 → breaches found
        if response.status_code == 200:
            breaches = response.json()

            # Extract only breach names (clean output)
            sites = [b["Name"] for b in breaches]

            return True, sites

        # 404 → no breaches
        elif response.status_code == 404:
            return False, []

        else:
            print(f"API returned {response.status_code} for {email}")
            return False, []

    except requests.exceptions.RequestException as e:
        print(f"Connection error while checking {email}: {str(e)}")
        return False, []
