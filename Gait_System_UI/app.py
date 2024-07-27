from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Mock user data (replace with actual database integration)
users = {
    'user@example.com': {
        'password': 'password123',
        'username': 'User',
        'email': 'user@example.com'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email]['password'] == password:
            session['username'] = users[email]['username']
            session['email'] = email
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message='Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'], employees=users[session['email']].get('employees', []))
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'], email=session['email'])
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
