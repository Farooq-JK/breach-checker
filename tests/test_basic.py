# test_basic.py
# Simple test for CSV reading

from csv_utils import read_emails

def test_read_emails(tmp_path):
    test_file = tmp_path / "emails.csv"
    test_file.write_text("test@example.com\n")

    emails = read_emails(test_file)
    assert emails == ["test@example.com"]
