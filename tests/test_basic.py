import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.csv_utils import read_emails


# Test case: file contains one email and a header
def test_read_emails(tmp_path):
    test_file = tmp_path / "emails.csv"
    test_file.write_text(
        "email_address\n"
        "test@example.com\n"
    )

    emails = read_emails(test_file)

    # The function should return a list with one email
    assert emails == ["test@example.com"]


# Test case: file contains only the header (no emails)
def test_read_emails_empty_file(tmp_path):
    test_file = tmp_path / "empty.csv"
    test_file.write_text("email_address\n")

    emails = read_emails(test_file)

    # The result should be an empty list
    assert emails == []


# Test case: file contains multiple emails
def test_read_emails_multiple(tmp_path):
    test_file = tmp_path / "many.csv"
    test_file.write_text(
        "email_address\n"
        "a@test.com\n"
        "b@test.com\n"
        "c@test.com\n"
    )

    emails = read_emails(test_file)

    # The function should return all emails in the correct order
    assert emails == ["a@test.com", "b@test.com", "c@test.com"]