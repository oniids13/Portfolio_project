from flask import Flask, abort, render_template, redirect, url_for, flash, request, get_flashed_messages
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Boolean
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
Bootstrap5(app)

def read_tasks():
    tasks = []
    try:
        with open('tasks.txt', 'r') as file:
            for line in file:
                description, done = line.strip().split('|')
                tasks.append({'description': description, 'done': done =='True'})
    except FileNotFoundError:
        pass
    return tasks

def write_tasks(tasks):
    with open('tasks.txt', 'w') as file:
        for task in tasks:
            file.write(f"{task['description']}|{task['done']}\n")
@app.route('/', methods=['GET', 'POST'])
def home():
    today = date.today()
    today = today.strftime("%m/%d/%Y")
    tasks = read_tasks()
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            tasks.append({'description': task, 'done': False})
        elif 'toggle' in request.form:
            task_index = int(request.form.get('toggle'))
            tasks[task_index]['done'] = not tasks[task_index]['done']
        elif 'delete' in request.form:
            task_index = int(request.form.get('delete'))
            tasks.pop(task_index)

        write_tasks(tasks)
        return redirect(url_for('home'))
    return render_template('index.html', date=today, tasks=tasks)

@app.route('/delete')
def delete():
    pass

if __name__ == '__main__':
    app.run(debug=True)