# allow tests to import project modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from csv_utils import read_emails


# Test 1: single email with header
def test_read_emails(tmp_path):
    test_file = tmp_path / "emails.csv"
    test_file.write_text(
        "email_address\n"
        "test@example.com\n"
    )

    emails = read_emails(test_file)

    assert emails == ["test@example.com"]


# Test 2: empty file but with header only
def test_read_emails_empty_file(tmp_path):
    test_file = tmp_path / "empty.csv"
    test_file.write_text("email_address\n")

    emails = read_emails(test_file)

    assert emails == []


# Test 3: multiple emails with header
def test_read_emails_multiple(tmp_path):
    test_file = tmp_path / "many.csv"
    test_file.write_text(
        "email_address\n"
        "a@test.com\n"
        "b@test.com\n"
        "c@test.com\n"
    )

    emails = read_emails(test_file)

    assert emails == ["a@test.com", "b@test.com", "c@test.com"]
