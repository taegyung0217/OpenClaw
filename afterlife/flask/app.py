from flask import Flask, request, session, redirect, url_for, render_template
import pymysql
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'db'), # 도커 환경이므로 'db'가 기본값인 것이 좋습니다.
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
        # SQL Injection 취약점 유지 (교육용)
        query = f"INSERT INTO souls (name, email, password_hash, alignment) VALUES ('{name}', '{email}', '{password}', '무')"
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
        # SQL Injection 취약점 유지 (교육용)
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
        cursor.execute("INSERT INTO posts (soul_id, title, content) VALUES (%s, %s, %s)",
                       (session['user_id'], title, content))
        db.commit()
        return redirect(url_for('board'))
    # [버그 수정 4] GET 요청 시 posts 없이 board.html 렌더링하면 템플릿에서 posts 변수 오류
    # → board()로 리다이렉트해서 posts를 정상적으로 넘기도록 수정
    # return render_template('board.html') 에서 아래로 수정
    return redirect(url_for('board'))
    


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
    cursor.execute("INSERT INTO comments (post_id, soul_id, content) VALUES (%s, %s, %s)",
        (post_id, session['user_id'], content))
    db.commit()
    return redirect(url_for('post', post_id=post_id))

# ── 직원 전용 기능 ──────────────────────────────────

@app.route('/employee/login', methods=['GET', 'POST'])
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

# ⭐ 추가된 성향 업데이트 기능
@app.route('/employee/update_alignment', methods=['POST'])
def update_alignment():
    if 'emp_id' not in session:
        return redirect(url_for('admin_login'))
    
    soul_id = request.form.get('soul_id')
    new_alignment = request.form.get('alignment') 
    # '선', '악', '무' 중 하나
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE souls SET alignment = %s WHERE id = %s", (new_alignment, soul_id))
    db.commit()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/employee/roulette', methods=['GET', 'POST'])
def admin_roulette():
    if 'emp_id' not in session:
        return redirect(url_for('admin_login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM souls")
    souls = cursor.fetchall()

    if request.method == 'POST':
        # [버그 수정 6] 룰렛 POST 시 결과 계산 없이 바로 리다이렉트하던 문제 수정
        # → 확률값을 받아 실제 랜덤 결과를 계산하고 roulette.html에 result를 넘김
        try:
            prob_human = float(request.form.get('prob_human', 0.33))
            prob_animal = float(request.form.get('prob_animal', 0.33))
            prob_plant = float(request.form.get('prob_plant', 0.34))
        except ValueError:
            prob_human, prob_animal, prob_plant = 0.33, 0.33, 0.34

        # 합계가 0이면 균등 배분
        total = prob_human + prob_animal + prob_plant
        if total <= 0:
            prob_human, prob_animal, prob_plant = 0.33, 0.33, 0.34
            total = 1.0

        rand = random.uniform(0, total)
        if rand < prob_human:
            result = 'human'
        elif rand < prob_human + prob_animal:
            result = 'animal'
        else:
            result = 'plant'

        return render_template('roulette.html', souls=souls, result=result)

    return render_template('roulette.html', souls=souls, result=None)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
