# Simple unit test to verify read_emails() works correctly

from csv_utils import read_emails


def test_read_emails(tmp_path):
    # create a temporary CSV file for testing
    test_file = tmp_path / "emails.csv"
    test_file.write_text("test@example.com\n")

    # function should return the email as a list
    emails = read_emails(test_file)
    assert emails == ["test@example.com"]
