from . import mail
from flask_mail import Message
from .models import Expense, Budget
from datetime import datetime
from sqlalchemy import func
from . import db

def check_budget_status(user_id, category):
    month = datetime.now().strftime('%Y-%m')
    total_spent = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id,
        Expense.category == category,
        func.strftime('%Y-%m', Expense.date) == month
    ).scalar() or 0

    budget = Budget.query.filter_by(user_id=user_id, category=category, month=month).first()
    if budget:
        if total_spent >= budget.amount:
            return f"You have exceeded your budget for {category}."
        elif total_spent >= 0.9 * budget.amount:
            return f"You're at 90% of your budget for {category}."
    return None

def send_budget_alert(to_email, message):
    msg = Message('Budget Alert', sender='noreply@expensetracker.com', recipients=[to_email])
    msg.body = message
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Email failed: {e}")
