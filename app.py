# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='A faire')
    archived = db.Column(db.Boolean, default=False)
    time_spent = db.Column(db.Float, default=0.0)  # Temps passé sur la tâche
    subtasks = db.relationship('SubTask', backref='task', lazy=True)

class SubTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='A faire')
    archived = db.Column(db.Boolean, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

@app.route('/')
def index():
    tasks = Task.query.filter_by(archived=False).order_by(
        db.case(
            (Task.status == 'A faire', 1),
            (Task.status == 'En cours', 2),
            (Task.status == 'Terminé', 3),
        ),
        Task.created_at
    ).all()
    return render_template('index.html', tasks=tasks)

@app.route('/calendar')
def calendar():
    tasks = Task.query.filter(Task.status == 'En cours').all()
    return render_template('calendar.html', tasks=tasks)

@app.route('/archived')
def archived():
    tasks = Task.query.filter_by(archived=True).order_by(Task.created_at).all()
    subtasks = SubTask.query.filter_by(archived=True).order_by(SubTask.created_at).all()
    return render_template('archived.html', tasks=tasks, subtasks=subtasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_subtask/<int:task_id>', methods=['POST'])
def add_subtask(task_id):
    title = request.form.get('title')
    new_subtask = SubTask(title=title, task_id=task_id)
    db.session.add(new_subtask)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    task = Task.query.get(task_id)
    task.status = request.form.get('status')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_subtask_status/<int:subtask_id>', methods=['POST'])
def update_subtask_status(subtask_id):
    subtask = SubTask.query.get(subtask_id)
    subtask.status = request.form.get('status')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/archive/<int:task_id>')
def archive(task_id):
    task = Task.query.get(task_id)
    task.archived = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/archive_subtask/<int:subtask_id>')
def archive_subtask(subtask_id):
    subtask = SubTask.query.get(subtask_id)
    subtask.archived = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/archive_completed_tasks')
def archive_completed_tasks():
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    tasks = Task.query.filter(Task.status == 'Terminé', Task.created_at <= one_month_ago).all()
    for task in tasks:
        task.archived = True
    subtasks = SubTask.query.filter(SubTask.status == 'Terminé', SubTask.created_at <= one_month_ago).all()
    for subtask in subtasks:
        subtask.archived = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_date/<string:type>/<int:id>', methods=['POST'])
def update_date(type, id):
    data = request.get_json()
    new_date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M')
    if type == 'task':
        task = Task.query.get(id)
        task.created_at = new_date
    elif type == 'subtask':
        subtask = SubTask.query.get(id)
        subtask.created_at = new_date
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)