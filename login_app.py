from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo

app = Flask(__name__)

# Secret key for session (used for flash messages)
app.secret_key = 'supersecretkey'

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/portifyDB"
mongo = PyMongo(app)

# ---------- ROUTES ----------

# Home Page (redirect to login for now)
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = mongo.db.users.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Sign-up Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = mongo.db.users.find_one({'username': username})
        
        if existing_user:
            flash('Username already exists. Try a different one.', 'error')
            return redirect(url_for('signup'))
        
        # Hash the password before saving it
        hashed_password = generate_password_hash(password)
        
        # Save the new user to the database
        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        })
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Dashboard (After successful login)
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"<h1>Welcome, {session['username']}!</h1><a href='/logout'>Logout</a>"
    else:
        flash('You need to log in first.', 'error')
        return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
