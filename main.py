# Entry point of the application (runs the full breach check process)

from csv_utils import read_emails, write_results
from api_client import check_email

# Input and output file names
INPUT_FILE = "email_list.csv"
OUTPUT_FILE = "output_result.csv"

# Read emails from CSV
emails = read_emails(INPUT_FILE)
results = []

print(f"Found {len(emails)} email(s) to check.")

# Check each email using the API
for email in emails:
    print(f"Checking: {email}")

    breached, sites = check_email(email)

    # Store result in dictionary format for CSV writing
    results.append({
        "email_address": email,
        "breached": breached,
        "site_where_breached": ";".join(sites)  # join multiple sites into one string
    })

# Save all results to output file
write_results(OUTPUT_FILE, results)

print(f"Done. Results saved to {OUTPUT_FILE}")
