# -------------------------------------------------
# Breach Checker - Main Application
# -------------------------------------------------

import time
import logging
import csv
import matplotlib.pyplot as plt  # used for chart visualisation

from csv_utils import read_emails, write_results
from api_client import check_email


# -------------------------------------------------
# Configuration
# -------------------------------------------------
INPUT_FILE = "email_list.csv"
OUTPUT_FILE = "output_result.csv"


# -------------------------------------------------
# Logging Configuration
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


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

    # Read results file and count values
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["breached"] == "True":
                breached += 1
            else:
                safe += 1

    # Chart data
    labels = ["Breached", "Safe"]
    values = [breached, safe]

    # Create bar chart
    plt.bar(labels, values)
    plt.title("Breach Summary")
    plt.ylabel("Number of Emails")

    # Save chart image
    plt.savefig("breach_summary.png")
    plt.close()

    logging.info("Chart saved to breach_summary.png")


# -------------------------------------------------
# Main Program Execution
# -------------------------------------------------
def main():
    """
    Main workflow:
    1. Read emails
    2. Check breaches
    3. Save results
    4. Generate chart
    """

    emails = read_emails(INPUT_FILE)
    results = []

    logging.info(f"Found {len(emails)} email(s) to check.")

    for email in emails:

        email = email.strip().lower()
        logging.info(f"Checking: {email}")

        try:
            # Call breach API
            breached, sites = check_email(email)

        except TimeoutError:
            # Retry once after delay
            logging.warning("Rate limited or timeout. Retrying...")
            time.sleep(5)
            breached, sites = check_email(email)

        except Exception as e:
            # Skip if serious error occurs
            logging.error(f"Error for {email}: {e}")
            continue

        # Store result
        results.append({
            "email_address": email,
            "breached": breached,
            "site_where_breached": ";".join(sites)
        })

        # Respect API rate limit
        time.sleep(1.6)

    # Save results to CSV
    write_results(OUTPUT_FILE, results)
    logging.info(f"Results saved to {OUTPUT_FILE}")

    # Generate summary chart
    create_breach_chart(OUTPUT_FILE)


# -------------------------------------------------
# Entry Point
# -------------------------------------------------
if __name__ == "__main__":
    main()
