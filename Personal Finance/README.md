# Expense Tracker App

## Features
- Add expenses with categories
- Set monthly budgets
- Alert when nearing or exceeding budget
- Email notifications
- Monthly reports

## How to Run (Locally)
1. Install dependencies:
pip install -r requirements.txt

2. Set environment variables:
export SECRET_KEY="your-key" export MAIL_USERNAME="your@gmail.com" export MAIL_PASSWORD="your-app-password"

3. Run:
python expense-tracker.py


## Docker
Build the image:
docker build -t expense-tracker . 

Run the container on port 5002:
docker run -p 5002:5000 expense-tracker

Then open http://localhost:5002