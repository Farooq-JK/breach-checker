# csv_utils.py
# Handles reading and writing CSV files

import csv

def read_emails(file_path):
    with open(file_path, newline="") as file:
        reader = csv.reader(file)
        return [row[0].strip() for row in reader if row]

def write_results(file_path, results):
    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["email_address", "breached", "site_where_breached"]
        )
        writer.writeheader()
        writer.writerows(results)
