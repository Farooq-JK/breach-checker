# allow tests to import project modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import requests
from unittest.mock import patch, Mock

from api_client import check_hibp


# -------------------------------------------------
# Test 1: 200 response (breached)
# -------------------------------------------------
@patch("api_client.requests.get")
def test_check_hibp_breached(mock_get):

    # Mock successful breach response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"Name": "Adobe"}, {"Name": "LinkedIn"}]
    mock_get.return_value = mock_response

    breached, sites = check_hibp("test@example.com")

    assert breached is True
    assert sites == ["Adobe", "LinkedIn"]


# -------------------------------------------------
# Test 2: 404 response (safe)
# -------------------------------------------------
@patch("api_client.requests.get")
def test_check_hibp_safe(mock_get):

    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    breached, sites = check_hibp("safe@example.com")

    assert breached is False
    assert sites == []


# -------------------------------------------------
# Test 3: 429 retry then success
# -------------------------------------------------
@patch("api_client.requests.get")
def test_check_hibp_retry(mock_get):

    mock_429 = Mock()
    mock_429.status_code = 429

    mock_200 = Mock()
    mock_200.status_code = 200
    mock_200.json.return_value = [{"Name": "Dropbox"}]

    # First call → 429, Second call → 200
    mock_get.side_effect = [mock_429, mock_200]

    breached, sites = check_hibp("retry@example.com")

    assert breached is True
    assert sites == ["Dropbox"]


# -------------------------------------------------
# Test 4: Network error handling
# -------------------------------------------------
@patch("api_client.requests.get")
def test_check_hibp_connection_error(mock_get):

    mock_get.side_effect = requests.exceptions.RequestException

    breached, sites = check_hibp("error@example.com")

    assert breached is False
    assert sites == []
