import flask
from flask import Flask, url_for, render_template, redirect, request, session, Blueprint, flash
import pickle, re
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "supa secret"

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    start = db.Column(db.Date)
    end = db.Column(db.Date)

with app.app_context():
    db.create_all()

@app.route('/', methods=["POST", "GET"])
@app.route('/home', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        button_id = int(request.form["id"])
        task_for_deletion = Task.query.filter_by(id=button_id).first()
        db.session.delete(task_for_deletion)
        db.session.commit()
        flash(f'Task {task_for_deletion.name} was successfully deleted!')
        return redirect(url_for("index"))
    else:
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks)

@app.route('/newtask', methods=["POST", "GET"])
def newtask():
    if request.method == "POST":
        name = request.form["InputName"]
        start = request.form["InputStart"]
        end = request.form["InputEnd"]
        task_for_addition = Task(name=name, start=datetime.strptime(start, '%Y-%m-%d'), end=datetime.strptime(end, '%Y-%m-%d'))
        db.session.add(task_for_addition)
        db.session.commit()
        flash(f'Task {task_for_addition.name} was successfully added!')
        return redirect(url_for("index"))
    else:
        return render_template("newtask.html")

@app.route('/calendar')
def calendar():
    import calendar_generator
    grouped_tasks = Task.query.group_by(Task.start)
    test_tasks = dict()
    for gtask in grouped_tasks:
        test_tasks[gtask.start] = Task.query.filter(Task.start == gtask.start)
    print(test_tasks)
    gen = calendar_generator.generateMonth
    calendar_generator.generateYearTable(gen, test_tasks)
    return render_template("calendar.html")

if __name__ == '__main__':
    app.run()