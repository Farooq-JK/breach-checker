# main.py
# Main program logic

from csv_utils import read_emails, write_results
from api_client import check_email

INPUT_FILE = "email_list.csv"
OUTPUT_FILE = "output_result.csv"

emails = read_emails(INPUT_FILE)
results = []

print(f"Found {len(emails)} email(s) to check.")

for email in emails:
    print(f"Checking: {email}")
    breached, sites = check_email(email)

    results.append({
        "email_address": email,
        "breached": breached,
        "site_where_breached": ";".join(sites)
    })

write_results(OUTPUT_FILE, results)
print(f"Done. Results saved to {OUTPUT_FILE}")
