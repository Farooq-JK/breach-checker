# Handles reading input emails and writing output results to CSV files

import csv


def read_emails(file_path):
    # Read first column from each row and return as a list of emails
    with open(file_path, newline="") as file:
        reader = csv.reader(file)
        return [row[0].strip() for row in reader if row]


def write_results(file_path, results):
    # Write results (list of dictionaries) into a CSV file
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["email_address", "breached", "site_where_breached"]
        )
        writer.writeheader()   # add column names
        writer.writerows(results)
