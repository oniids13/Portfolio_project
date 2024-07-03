from flask import Flask, abort, render_template, redirect, url_for, flash, request, get_flashed_messages
from flask_bootstrap import Bootstrap5
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
Bootstrap5(app)

def read_tasks():
    tasks = []
    done_tasks = []
    try:
        with open('tasks.txt', 'r') as file:
            for line in file:
                description, done = line.strip().split('|')
                if done == 'True':
                    done_tasks.append({'description': description, 'done': True})
                else:
                    tasks.append({'description': description, 'done': False})
    except FileNotFoundError:
        pass
    return tasks, done_tasks

def write_tasks(tasks, done_tasks):
    with open('tasks.txt', 'w') as file:
        for task in tasks + done_tasks:
            file.write(f"{task['description']}|{task['done']}\n")
@app.route('/', methods=['GET', 'POST'])
def home():
    today = date.today()
    today = today.strftime("%m/%d/%Y")
    year = date.today()
    year = year.year
    tasks, done_tasks = read_tasks()
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            tasks.append({'description': task, 'done': False})
        elif 'toggle' in request.form:
            task_index = int(request.form.get('toggle'))
            tasks[task_index]['done'] = not tasks[task_index]['done']
            if tasks[task_index]['done']:
                done_tasks.append(tasks.pop(task_index))
        elif 'delete' in request.form:
            task_index = int(request.form.get('delete'))
            section = request.form.get('section')
            if section == 'tasks':
                tasks.pop(task_index)
            elif section == 'done_tasks':
                done_tasks.pop(task_index)

        write_tasks(tasks, done_tasks)
        return redirect(url_for('home'))
    return render_template('index.html', date=today, tasks=tasks, done_tasks=done_tasks, year=year)


if __name__ == '__main__':
    app.run(debug=True)