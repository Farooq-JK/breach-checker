import csv

# Read email addresses from CSV file
def read_emails(file_path):

    emails = []

    # Open the input file
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Uses header row

        # Loop through rows and collect valid emails
        for row in reader:
            email = row.get("email_address")

            # Only add non-empty emails
            if email and email.strip():
                emails.append(email.strip())

    return emails


# Write breach results to CSV file
def write_results(file_path, results):

    # Open output file in write mode
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["email_address", "breached", "site_where_breached"]
        )

        writer.writeheader()      # Write column names
        writer.writerows(results) # Write result rows
