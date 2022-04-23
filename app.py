from pprint import pprint
from flask import Flask, render_template, request
import database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/tasks_entry.html', methods=['GET', 'POST'])
def tasks_entry():
    name = None
    creators = None
    description = None
    start_date = None
    completion_date = None
    due_date = None
    priority = None
    assigned_to = None
    project_file = None
    status = None
    if request.method == "POST":
        name = request.form.get("name")
        creators = request.form.get("creators")
        description = request.form.get("description")
        start_date = request.form.get("start_date")
        completion_date = request.form.get("completion_date")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")
        assigned_to = request.form.get("assigned_to")
        project_file = request.form.get("project_file")
        status = request.form.get("status")
    return render_template('tasks_entry.html',
        name = name,
        creators = creators,
        description = description,
        start_date = start_date,
        completion_date = completion_date,
        due_date = due_date,
        priority = priority,
        assigned_to = assigned_to,
        project_file = project_file,
        status = status,
    )

@app.route('/tasks_view.html', methods=['GET', 'POST'])
def tasks_view():
    selected_creator = None
    creators_tasks = None
    if request.method == "POST":
        selected_creator = request.form.get("creators")
        creators_tasks = database.view_all_tasks_by_creators(selected_creator)
    return render_template('tasks_view.html', 
    all_tasks = database.view_all_tasks(),
    all_creators = database.get_all_creators(),
    selected_creator = selected_creator,
    creators_tasks = creators_tasks,
    )


MENU = """Please select one of the following options:
1) View tasks
2) Create task
3) Update task
4) Delete task
5) Exit.

Your selection: """


def main_menu():
    # use for testing
    while (user_input := input(MENU)):
        if user_input == "1":
            pprint(database.view_all_tasks())
        elif user_input == "2":
            database.create_task()
        elif user_input == "3":
            database.update_task()
        elif user_input == "4":
            database.delete_task()
        elif user_input == "5":
            break
        else:
            print("Invalid input, please try again!")


if __name__ == "__main__":
    app.run(debug=True)
    # main_menu()
