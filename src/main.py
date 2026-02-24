import time
import logging
import csv
import matplotlib.pyplot as plt

from src.csv_utils import read_emails, write_results
from src.api_client import check_email
from src.config import POLITE_DELAY, SUMMARY_CHART


# Basic logging setup (shows time, level, and message)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Input and output file names
INPUT_FILE = "email_list.csv"
OUTPUT_FILE = "output_result.csv"


# Generate a simple bar chart showing breached vs safe emails
def create_breach_chart(csv_file):

    breached = 0
    safe = 0

    # Read the results file and count breached vs safe
    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["breached"] == "True":
                breached += 1
            else:
                safe += 1

    # Create and save the chart
    plt.bar(["Breached", "Safe"], [breached, safe])
    plt.title("Breach Summary")
    plt.ylabel("Number of Emails")
    plt.savefig(SUMMARY_CHART)
    plt.close()

    logging.info(f"Chart saved to {SUMMARY_CHART}")


# Main program flow
def main():

    # Read emails from the input file
    emails = read_emails(INPUT_FILE)
    results = []

    logging.info(f"Found {len(emails)} email(s) to check.")

    # Check each email one by one
    for email in emails:
        email = email.strip().lower()
        logging.info(f"Checking: {email}")

        breached, sites = check_email(email)

        # Store the result in a dictionary
        results.append({
            "email_address": email,
            "breached": breached,
            "site_where_breached": ";".join(sites)
        })

        # Small delay to avoid hitting API rate limits
        time.sleep(POLITE_DELAY)

    # Save results to CSV
    write_results(OUTPUT_FILE, results)
    logging.info(f"Results saved to {OUTPUT_FILE}")

    # Create summary chart from results
    create_breach_chart(OUTPUT_FILE)


# Run the program only if this file is executed directly
if __name__ == "__main__":
    main()