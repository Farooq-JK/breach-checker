import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
from unittest.mock import patch, Mock

from src.api_client import check_hibp


# Test case: API returns 200 (email found in breaches)
@patch("src.api_client.requests.get")
def test_check_hibp_breached(mock_get):

    # Create a fake successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"Name": "Adobe"}, {"Name": "LinkedIn"}]
    mock_get.return_value = mock_response

    breached, sites = check_hibp("test@example.com")

    # Check that the function detects the breach correctly
    assert breached is True
    assert sites == ["Adobe", "LinkedIn"]


# Test case: API returns 404 (email not found)
@patch("src.api_client.requests.get")
def test_check_hibp_safe(mock_get):

    # Fake response for a safe email
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    breached, sites = check_hibp("safe@example.com")

    # The function should return False and an empty list
    assert breached is False
    assert sites == []


# Test case: First attempt hits rate limit (429), second attempt succeeds
@patch("src.api_client.requests.get")
def test_check_hibp_retry(mock_get):

    # Simulate rate limit response
    mock_429 = Mock()
    mock_429.status_code = 429

    # Simulate successful response after retry
    mock_200 = Mock()
    mock_200.status_code = 200
    mock_200.json.return_value = [{"Name": "Dropbox"}]

    # First call returns 429, second call returns 200
    mock_get.side_effect = [mock_429, mock_200]

    breached, sites = check_hibp("retry@example.com")

    # The function should retry and then return success
    assert breached is True
    assert sites == ["Dropbox"]


# Test case: Network or connection error occurs
@patch("src.api_client.requests.get")
def test_check_hibp_connection_error(mock_get):

    # Simulate a request exception
    mock_get.side_effect = requests.exceptions.RequestException

    breached, sites = check_hibp("error@example.com")

    # The function should handle the error safely
    assert breached is False
    assert sites == []