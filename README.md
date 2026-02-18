# Breach Checker -- Email Breach Screening Tool

## Overview

Breach Checker is a Python command-line application that checks email
addresses against the Have I Been Pwned (HIBP) API and reports whether
they appear in known data breaches.

The project demonstrates clean structure, secure configuration, testing,
and CI integration.

------------------------------------------------------------------------

## Key Features

-   HIBP API integration
-   Secure API key using `.env`
-   Configurable settings via `config.yaml`
-   Retry and rate-limit handling (HTTP 429)
-   Structured logging
-   CSV input and output
-   Unit testing with pytest
-   Mocked API testing
-   GitHub Actions CI

------------------------------------------------------------------------

## Project Structure

    breach_checker/
    │
    ├── src/
    │   ├── main.py
    │   ├── api_client.py
    │   ├── csv_utils.py
    │   ├── config.py
    │   └── __init__.py
    │
    ├── config.yaml
    ├── email_list.csv
    ├── output_result.csv
    │
    ├── tests/
    │   ├── test_basic.py
    │   └── test_api.py
    │
    ├── .github/workflows/tests.yml
    ├── requirements.txt
    ├── README.md
    ├── .env.example
    ├── .gitignore

------------------------------------------------------------------------

## Installation

Create a virtual environment:

**Windows**

``` bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux**

``` bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Configuration

Create a `.env` file:

``` bash
HIBP_API_KEY=your_api_key_here
```

Example `config.yaml`:

``` yaml
timeout: 10
max_retries: 4
retry_delay: 3
```

------------------------------------------------------------------------

## Usage

``` bash
python -m src.main
```

Input: `email_list.csv`
Output: `output_result.csv`
Chart: `breach_summary.png`

------------------------------------------------------------------------

## Testing

Run:

``` bash
pytest -v
```

Tests include:

-   CSV validation
-   200 / 404 responses
-   429 retry logic
-   Network error handling

------------------------------------------------------------------------

## Continuous Integration

GitHub Actions automatically installs dependencies and runs tests on
every push.

------------------------------------------------------------------------

## Security

-   No hardcoded secrets
-   API key stored in `.env`
-   `.env` excluded from Git

------------------------------------------------------------------------

## Dependencies

-   requests
-   python-dotenv
-   pyyaml
-   pytest
-   matplotlib
