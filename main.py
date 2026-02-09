# Entry point of the application (runs the full breach check process)

import time
import logging  # ✅ professional logging instead of print()

from csv_utils import read_emails, write_results
from api_client import check_email


# -------------------------------------------------
# Logging configuration
# INFO = normal progress messages
# WARNING = recoverable issues
# ERROR = serious problems
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Input and output file names
INPUT_FILE = "email_list.csv"
OUTPUT_FILE = "output_result.csv"


# Read emails from CSV
emails = read_emails(INPUT_FILE)
results = []

# ✅ was print() → now logging
logging.info(f"Found {len(emails)} email(s) to check.")


# Check each email using the API (one-by-one only)
for email in emails:

    # ✅ clean email (avoids matching problems)
    email = email.strip().lower()

    logging.info(f"Checking: {email}")

    try:
        # ✅ call API normally
        breached, sites = check_email(email)

    except Exception:
        # ✅ recoverable issue → WARNING level
        logging.warning("Rate limit hit. Waiting and retrying...")
        time.sleep(5)
        breached, sites = check_email(email)

    # Store result in dictionary format for CSV writing
    results.append({
        "email_address": email,
        "breached": breached,
        "site_where_breached": ";".join(sites)
    })

    # ✅ slow down between requests (rate limiting)
    time.sleep(1.6)


# Save all results to output file
write_results(OUTPUT_FILE, results)

logging.info(f"Done. Results saved to {OUTPUT_FILE}")
