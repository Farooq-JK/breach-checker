# -------------------------------------------------
# Entry point of the application
# -------------------------------------------------

import time
import logging
import csv
import matplotlib.pyplot as plt

from csv_utils import read_emails, write_results
from api_client import check_email
from config import POLITE_DELAY, SUMMARY_CHART


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

INPUT_FILE = "email_list.csv"
OUTPUT_FILE = "output_result.csv"


# -------------------------------------------------
# Create breach summary chart
# -------------------------------------------------
def create_breach_chart(csv_file):
    """
    Reads the output CSV file and generates
    a bar chart showing breached vs safe emails.
    """

    breached = 0
    safe = 0

    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["breached"] == "True":
                breached += 1
            else:
                safe += 1

    plt.bar(["Breached", "Safe"], [breached, safe])
    plt.title("Breach Summary")
    plt.ylabel("Number of Emails")
    plt.savefig(SUMMARY_CHART)
    plt.close()

    logging.info(f"Chart saved to {SUMMARY_CHART}")


# -------------------------------------------------
# Main execution
# -------------------------------------------------
def main():
    emails = read_emails(INPUT_FILE)
    results = []

    logging.info(f"Found {len(emails)} email(s) to check.")

    for email in emails:
        email = email.strip().lower()
        logging.info(f"Checking: {email}")

        breached, sites = check_email(email)

        results.append({
            "email_address": email,
            "breached": breached,
            "site_where_breached": ";".join(sites)
        })

        time.sleep(POLITE_DELAY)

    write_results(OUTPUT_FILE, results)
    logging.info(f"Results saved to {OUTPUT_FILE}")

    create_breach_chart(OUTPUT_FILE)


# Run application
if __name__ == "__main__":
    main()
