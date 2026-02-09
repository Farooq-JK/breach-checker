# Entry point of the application (runs the full breach check process)

import time  # ✅ used to slow down requests (prevents 429 rate limit)

from csv_utils import read_emails, write_results
from api_client import check_email

# Input and output file names
INPUT_FILE = "email_list.csv"
OUTPUT_FILE = "output_result.csv"

# Read emails from CSV
emails = read_emails(INPUT_FILE)
results = []

print(f"Found {len(emails)} email(s) to check.")

# Check each email using the API (one-by-one only)
for email in emails:
    # ✅ clean email (avoids matching problems)
    email = email.strip().lower()

    print(f"Checking: {email}")

    try:
        # ✅ call API normally
        breached, sites = check_email(email)

    except Exception:
        # ✅ simple retry if something like 429 happens
        print("Rate limit hit. Waiting and retrying...")
        time.sleep(5)  # wait longer before retry
        breached, sites = check_email(email)

    # Store result in dictionary format for CSV writing
    results.append({
        "email_address": email,
        "breached": breached,
        "site_where_breached": ";".join(sites)
    })

    # ✅ IMPORTANT: slow down between requests (HIBP requirement)
    time.sleep(1.6)   # about 1–2 requests per second max


# Save all results to output file
write_results(OUTPUT_FILE, results)

print(f"Done. Results saved to {OUTPUT_FILE}")
