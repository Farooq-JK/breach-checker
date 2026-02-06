# Email Breach Checker

This is a small Python application that checks if email addresses have been exposed in data breaches using the Have I Been Pwned (HIBP) API.

The program:
- reads emails from a CSV file
- checks each email using the API
- saves the results to another CSV file

---

## Project Files

main.py → runs the program  
api_client.py → connects to the API  
csv_utils.py → reads/writes CSV files  
config.py → loads API key  
email_list.csv → input emails  
output_result.csv → results  
.env → stores your API key
.env.example → template file  

---

## Setup

### 1. Create virtual environment

Windows:
python -m venv .venv
.venv\Scripts\activate

Mac/Linux:
python -m venv .venv
source .venv/bin/activate

---

### 2. Install packages

pip install -r requirements.txt

---

### 3. Add your API key

Create a file called `.env` in the project folder:

HIBP_API_KEY=your_api_key_here

---

## Run

python main.py

---

## Input (email_list.csv)

example@example.com
test@gmail.com

---

## Output (output_result.csv)

email_address, breached, site_where_breached

---

## Test

pytest

---

## Notes

- Do not share your API key
- Keep the .env file private
- This project is for learning purposes
