from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'afterlife_secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username') == 'reaper' and request.form.get('password') == '1234':
            session['reaper_auth'] = True
            return redirect(url_for('dashboard'))
        return render_template('employee/admin_login.html', error="틀렸소.")
    return render_template('employee/admin_login.html')

@app.route('/employee/dashboard')
def dashboard():
    if not session.get('reaper_auth'):
        return redirect(url_for('admin_login'))
    souls = [
        {"name": "홍길동", "deed": "빈민 구제", "is_evil": False},
        {"name": "놀부", "deed": "재산 갈취", "is_evil": True}
    ]
    return render_template('employee/dashboard.html', souls=souls)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)





















from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'afterlife_secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username') == 'reaper' and request.form.get('password') == '1234':
            session['reaper_auth'] = True
            return redirect(url_for('dashboard'))
        return render_template('employee/admin_login.html', error="틀렸소.")
    return render_template('employee/admin_login.html')

@app.route('/employee/dashboard')
def dashboard():
    if not session.get('reaper_auth'):
        return redirect(url_for('admin_login'))
    souls = [
        {"name": "홍길동", "deed": "빈민 구제", "is_evil": False},
        {"name": "놀부", "deed": "재산 갈취", "is_evil": True}
    ]
    return render_template('employee/dashboard.html', souls=souls)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
