import csv


# Read email addresses from a CSV file
def read_emails(file_path):

    emails = []

    # Open the file and read it using the header row
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Go through each row and collect valid email addresses
        for row in reader:
            email = row.get("email_address")

            # Ignore empty or blank values
            if email and email.strip():
                emails.append(email.strip())

    return emails


# Save breach check results into a new CSV file
def write_results(file_path, results):

    # Create or overwrite the output file
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["email_address", "breached", "site_where_breached"]
        )

        # Write column headers first
        writer.writeheader()

        # Write all result rows to the file
        writer.writerows(results)