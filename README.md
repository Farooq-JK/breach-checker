
# Breach Checker – Email Breach Screening Tool

## Overview
Breach Checker is a simple Python command‑line application that checks multiple email addresses against the Have I Been Pwned (HIBP) API and reports whether they appear in known data breaches.

The project demonstrates:
- API integration
- secure environment variables (.env)
- logging
- retry + rate limiting
- unit testing with pytest
- Continuous Integration with GitHub Actions
- clean modular design

---

## Full Project Structure

breach_checker/
│
├── main.py                     # entry point – runs full workflow
├── api_client.py               # sends requests to HIBP API
├── csv_utils.py                # reads input CSV & writes results CSV
├── config.py                   # loads API key from .env safely
│
├── email_list.csv              # input emails (sample data)
├── output_result.csv           # generated results (auto-created)
│
├── tests/
│   └── test_basic.py           # pytest unit tests for CSV logic
│
├── .github/workflows/
│   └── tests.yml               # GitHub Actions CI workflow (auto tests)
│
├── requirements.txt            # dependencies list
├── README.md                   # documentation
│
├── .env                        # API key (private – NOT committed)
├── .env.example                # template for API key
├── .gitignore                  # ignores secrets, cache, venv
│
└── .venv/                      # virtual environment (local only)

---

## Installation

### 1. Create virtual environment
Windows:
python -m venv .venv
.venv\Scripts\activate

Mac/Linux:
python -m venv .venv
source .venv/bin/activate

### 2. Install packages
pip install -r requirements.txt

---

## Configuration

Create a .env file:

HIBP_API_KEY=your_api_key_here

Never upload this file to GitHub.

---

## Usage

Run:
python main.py

Input:
email_list.csv

Output:
output_result.csv

---

## Testing

Run locally:
pytest -v

Tests check:
- single email
- empty file
- multiple emails

---

## Continuous Integration (CI)

This project uses **GitHub Actions** to automatically run tests every time code is pushed to GitHub.

It will:
- install dependencies
- run `pytest`
- show a green ✓ if tests pass
- show a red ✗ if tests fail

This helps make sure the application always works correctly.

Workflow file:
.github/workflows/tests.yml

---

## Logging

The application uses Python logging instead of print():
- INFO → progress messages
- WARNING → recoverable issues
- ERROR → failures

Example:
2026-02-10 18:22:01 - INFO - Checking: test@example.com

---

## Security Practices
- API key stored in .env only
- .env ignored by git
- no hardcoded secrets
- request timeouts
- retry on 429 rate limits
- structured outputs

---

## Dependencies
- requests
- python-dotenv
- pytest

Install with:
pip install -r requirements.txt

---

## Author
Farooq
