# Handles communication with the Have I Been Pwned API

import requests
from config import API_KEY, BASE_URL


def check_email(email):
    """
    Check one email against the API.

    Returns:
        (True, [breach names])  -> if breached
        (False, [])            -> if safe or error
    """

    # Required headers for the API request
    headers = {
        "hibp-api-key": API_KEY,
        "user-agent": "breach-checker-app"
    }

    try:
        # Send GET request to HIBP endpoint
        response = requests.get(
            f"{BASE_URL}/breachedaccount/{email}",
            headers=headers,
            timeout=10
        )

        # If breaches exist
        if response.status_code == 200:
            breaches = response.json()

            # Keep only breach names for cleaner output
            sites = [b["Name"] for b in breaches]
            return True, sites

        # If no breaches found
        elif response.status_code == 404:
            return False, []

        # Any other unexpected response
        else:
            print(f"API returned {response.status_code} for {email}")
            return False, []

    # Handle network/connection errors safely
    except requests.exceptions.RequestException as e:
        print(f"Connection error while checking {email}: {str(e)}")
        return False, []
