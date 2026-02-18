import csv


def read_emails(file_path):
    """
    Read email addresses from a CSV file with a header.
    Expects a column named 'email_address'.
    Returns a list of cleaned email strings.
    """
    emails = []

    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Automatically uses header row

        for row in reader:
            email = row.get("email_address")

            # Ensure value exists and is not empty
            if email and email.strip():
                emails.append(email.strip())

    return emails


def write_results(file_path, results):
    """
    Write results (list of dictionaries) into a CSV file.
    Each dictionary must contain:
    - email_address
    - breached
    - site_where_breached
    """
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["email_address", "breached", "site_where_breached"]
        )

        writer.writeheader()   # Add column names
        writer.writerows(results)
