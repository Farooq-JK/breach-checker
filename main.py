# Entry point of the application (runs the full breach check process)
import time
import logging
import csv                      # ✅ for reading results CSV
import matplotlib.pyplot as plt  # ✅ for chart visualisation
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
# -------------------------------------------------
# ✅ NEW: simple visualisation function
# Creates bar chart: breached vs safe emails
# Saves image as breach_summary.png
# -------------------------------------------------
def create_breach_chart(csv_file):
    breached = 0
    safe = 0
    # Read output CSV and count results
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

    # Save image (important for CLI apps)
    plt.savefig("breach_summary.png")
    plt.close()

    logging.info("Chart saved to breach_summary.png")
# -------------------------------------------------
# Main process
# -------------------------------------------------
# Read emails from CSV
emails = read_emails(INPUT_FILE)
results = []

logging.info(f"Found {len(emails)} email(s) to check.")


# Check each email using the API (one-by-one only)
for email in emails:

    email = email.strip().lower()
    logging.info(f"Checking: {email}")

    try:
        breached, sites = check_email(email)

    except Exception:
        logging.warning("Rate limit hit. Waiting and retrying...")
        time.sleep(5)
        breached, sites = check_email(email)

    results.append({
        "email_address": email,
        "breached": breached,
        "site_where_breached": ";".join(sites)
    })

    time.sleep(1.6)

# Save all results to output file
write_results(OUTPUT_FILE, results)

logging.info(f"Done. Results saved to {OUTPUT_FILE}")

# -------------------------------------------------
# ✅ NEW: generate visual summary chart
# -------------------------------------------------
create_breach_chart(OUTPUT_FILE)
