from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'secret')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://mongo:27017/bank_app')
mongo = PyMongo(app)

@app.route('/banking/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name  = request.form.get('last_name')
        email      = request.form.get('email')
        password   = request.form.get('password')
        if not (first_name and last_name and email and password):
            flash('Please fill all fields', 'error')
            return redirect(url_for('register'))
        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            flash('Email already exists', 'error')
            return redirect(url_for('register'))
        password_hash = generate_password_hash(password)
        user = {
            'first_name': first_name,
            'last_name':  last_name,
            'email':      email,
            'password_hash': password_hash,
            'balance':      0.0,
            'transactions': []
        }
        mongo.db.users.insert_one(user)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/banking/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        user = mongo.db.users.find_one({'email': email})
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = str(user['_id'])
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/banking/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
    return render_template('dashboard.html', user=user)

@app.route('/banking/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    amount = request.form.get('amount')
    try:
        amount = float(amount)
    except:
        flash('Invalid amount', 'error')
        return redirect(url_for('dashboard'))
    if amount <= 0:
        flash('Amount must be positive', 'error')
        return redirect(url_for('dashboard'))
    if amount > 10000:
        flash('Amount > 10,000 requires OTP (skipped).', 'info')
    user_id = session['user_id']
    user    = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    new_balance = user['balance'] + amount
    txn = {'type': 'deposit', 'amount': amount}
    mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'balance': new_balance}, '$push': {'transactions': txn}}
    )
    flash('Deposit successful', 'success')
    return redirect(url_for('dashboard'))

@app.route('/banking/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    amount = request.form.get('amount')
    try:
        amount = float(amount)
    except:
        flash('Invalid amount', 'error')
        return redirect(url_for('dashboard'))
    if amount <= 0:
        flash('Amount must be positive', 'error')
        return redirect(url_for('dashboard'))
    user_id = session['user_id']
    user    = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user['balance'] < amount:
        flash('Insufficient funds', 'error')
        return redirect(url_for('dashboard'))
    new_balance = user['balance'] - amount
    txn = {'type': 'withdrawal', 'amount': amount}
    mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'balance': new_balance}, '$push': {'transactions': txn}}
    )
    flash('Withdrawal successful', 'success')
    return redirect(url_for('dashboard'))

@app.route('/banking/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
