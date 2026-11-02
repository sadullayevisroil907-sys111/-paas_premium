from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            guruh TEXT NOT NULL,
            ball INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        guruh = request.form.get('guruh')
        ball = request.form.get('ball')
        
        if name and guruh and ball:
            conn = sqlite3.connect('students.db')
            c = conn.cursor()
            c.execute('INSERT INTO students (name, guruh, ball) VALUES (?, ?, ?)', (name, guruh, int(ball)))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()

    total_students = len(students)
    avg_score = round(sum(student[3] for student in students) / total_students, 1) if total_students > 0 else 0
    total_groups = len(set(student[2] for student in students))

    return render_template('index.html', students=students, total=total_students, avg=avg_score, groups=total_groups)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
  
