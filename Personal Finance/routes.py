from flask import Blueprint, request, jsonify, render_template
from .models import db, User, Expense, Budget
from .utils import send_budget_alert, check_budget_status
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.form
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        user = User(email=data['email'])
        db.session.add(user)
        db.session.commit()
    expense = Expense(user_id=user.id, category=data['category'], amount=float(data['amount']))
    db.session.add(expense)
    db.session.commit()
    
    # Check budget status
    alert_msg = check_budget_status(user.id, data['category'])
    if alert_msg:
        send_budget_alert(user.email, alert_msg)

    return 'Expense Added'

@main.route('/set_budget', methods=['POST'])
def set_budget():
    data = request.form
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        user = User(email=data['email'])
        db.session.add(user)
        db.session.commit()
    month = datetime.now().strftime('%Y-%m')
    budget = Budget(user_id=user.id, category=data['category'], amount=float(data['amount']), month=month)
    db.session.add(budget)
    db.session.commit()
    return 'Budget Set'

@main.route('/report', methods=['GET'])
def report():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return 'User not found', 404
    month = datetime.now().strftime('%Y-%m')
    report_data = []
    for budget in user.budgets:
        if budget.month == month:
            spent = sum(e.amount for e in user.expenses if e.category == budget.category and e.date.strftime('%Y-%m') == month)
            report_data.append({
                'category': budget.category,
                'budget': budget.amount,
                'spent': spent
            })
    return jsonify(report_data)
