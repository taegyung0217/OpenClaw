from flask import Flask, request, session, redirect, url_for, render_template
import pymysql
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        user=os.environ.get('DB_USER', 'soul'),
        password=os.environ.get('DB_PASSWORD', 'soul1234'),
        database=os.environ.get('DB_NAME', 'afterlife'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# ── 메인 ──────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ── 회원가입 ───────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        # 취약점: SQL injection (password 미sanitize)
        query = f"INSERT INTO souls (name, email, password_hash) VALUES ('{name}', '{email}', '{password}')"
        cursor.execute(query)
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# ── 로그인 ─────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        # 취약점: SQL injection (로그인 bypass 가능)
        query = f"SELECT * FROM souls WHERE email='{email}' AND password_hash='{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['name'] = user['name']
            return redirect(url_for('index'))
        return render_template('login.html', error='로그인 실패')
    return render_template('login.html')

# ── 로그아웃 ───────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ── 환생 대기열 ────────────────────────────────
@app.route('/queue', methods=['GET', 'POST'])
def queue():
    if request.method == 'POST':
        soul_id = request.form.get('soul_id', session.get('user_id', 1))
        db = get_db()
        cursor = db.cursor()
        # 취약점: soul_id 검증 없음 → 다른 사람 번호표 발급 가능
        cursor.execute(f"INSERT INTO queue_tickets (soul_id, ticket_number) VALUES ({soul_id}, FLOOR(RAND()*9000)+1000)")
        db.commit()
        cursor.execute(f"SELECT * FROM queue_tickets WHERE soul_id={soul_id} ORDER BY issued_at DESC LIMIT 1")
        ticket = cursor.fetchone()
        return render_template('queue.html', ticket=ticket)
    return render_template('queue.html', ticket=None)

# ── 게시판 ─────────────────────────────────────
@app.route('/board')
def board():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT posts.*, souls.name FROM posts JOIN souls ON posts.soul_id=souls.id ORDER BY created_at DESC")
    posts = cursor.fetchall()
    return render_template('board.html', posts=posts)

@app.route('/board/write', methods=['GET', 'POST'])
def write():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db = get_db()
        cursor = db.cursor()
        # 취약점: XSS (content sanitize 없음)
        cursor.execute("INSERT INTO posts (soul_id, title, content) VALUES (%s, %s, %s)",
                       (session['user_id'], title, content))
        db.commit()
        return redirect(url_for('board'))
    return render_template('board.html')

@app.route('/board/<int:post_id>')
def post(post_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT posts.*, souls.name FROM posts JOIN souls ON posts.soul_id=souls.id WHERE posts.id=%s", (post_id,))
    post = cursor.fetchone()
    cursor.execute("SELECT comments.*, souls.name FROM comments JOIN souls ON comments.soul_id=souls.id WHERE post_id=%s", (post_id,))
    comments = cursor.fetchall()
    return render_template('post.html', post=post, comments=comments)

@app.route('/board/<int:post_id>/comment', methods=['POST'])
def comment(post_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    content = request.form['content']
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO comments (post_id, soul_id, content) VALUES (%s, %s, %s)",
        (post_id, session['user_id'], content)
    )
    db.commit()

    return redirect(url_for('post', post_id=post_id))


    
    
##########

    
# ── 직원 전용 기능 ──────────────────────────────────

@app.route('/employee/login', methods=['GET', 'POST'])  # /admin/login → /employee/login 으로 통일
def admin_login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        db = get_db()
        cursor = db.cursor()
        query = f"SELECT * FROM employees WHERE name='{name}' AND password_hash='{password}'"
        cursor.execute(query)
        employee = cursor.fetchone()
        if employee:
            session['emp_id'] = employee['id']
            session['emp_name'] = employee['name']
            session['emp_rank'] = employee['position']
            return redirect(url_for('admin_dashboard'))
        return render_template('employee/admin_login.html', error="인증 정보가 올바르지 않습니다.")
    return render_template('employee/admin_login.html')


@app.route('/employee/dashboard')
def admin_dashboard():
    if 'emp_id' not in session:
        return redirect(url_for('admin_login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM souls")
    souls = cursor.fetchall()
    return render_template('employee/dashboard.html', souls=souls)


@app.route('/employee/roulette', methods=['GET', 'POST'])
def admin_roulette():
    if 'emp_id' not in session:
        return redirect(url_for('admin_login'))
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        return redirect(url_for('admin_dashboard'))
    cursor.execute("SELECT * FROM souls")
    souls = cursor.fetchall()
    return render_template('employee/roulette.html', souls=souls)


# 파일 맨 마지막
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
