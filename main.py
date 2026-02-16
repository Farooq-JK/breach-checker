import time
import logging
import csv                      # read CSV results
import matplotlib.pyplot as plt  # chart visualisation

from csv_utils import read_emails, write_results
from api_client import check_email


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Input and output files
INPUT_FILE = "email_list.csv"
OUTPUT_FILE = "output_result.csv"

# Read emails from CSV
emails = read_emails(INPUT_FILE)
results = []

logging.info(f"Found {len(emails)} email(s) to check.")

# Check each email one-by-one
for email in emails:

    email = email.strip().lower()

    # INFO → normal progress
    logging.info(f"Checking: {email}")

    try:
        # Call API
        breached, sites = check_email(email)

    # WARNING → temporary issue (retry)
    except TimeoutError:
        logging.warning("Rate limited or timeout. Waiting before retry...")
        time.sleep(5)
        breached, sites = check_email(email)

    # ERROR → serious failure (skip email)
    except Exception as e:
        logging.error(f"Connection error occurred for {email}: {e}")
        continue   # skip this email and move on

    # Save result
    results.append({
        "email_address": email,
        "breached": breached,
        "site_where_breached": ";".join(sites)
    })

    # polite delay to respect API limits
    time.sleep(1.6)

# Save results
write_results(OUTPUT_FILE, results)

logging.info(f"Done. Results saved to {OUTPUT_FILE}")

# Create simple breach summary chart
def create_breach_chart(csv_file):
    breached = 0
    safe = 0

    # Count breached vs safe emails
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["breached"] == "True":
                breached += 1
            else:
                safe += 1

    labels = ["Breached", "Safe"]
    values = [breached, safe]

    # Create bar chart
    plt.bar(labels, values)
    plt.title("Breach Summary")
    plt.ylabel("Number of Emails")

    # Save chart to file
    plt.savefig("breach_summary.png")
    plt.close()

    logging.info("Chart saved to breach_summary.png")

# Generate visual summary chart
create_breach_chart(OUTPUT_FILE)
