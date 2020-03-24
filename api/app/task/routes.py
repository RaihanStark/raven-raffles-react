from app.task import blueprint
from flask import request, render_template
from app.task.util import add_task, get_all_tasks, delete_task, start_tasks_raffle
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)


@blueprint.route('/v1/tasks', methods=['GET', 'POST', 'DELETE'])
@login_required
def tasks():
    if request.method == 'GET':
        return get_all_tasks()
    elif request.method == 'POST':
        # # return {'data':'mam'}
        print(request.form)
        return add_task(request.form['sites'],
                        request.form['shoename'],
                        request.form['shoeurl'],
                        request.form['shoeentries'],
                        request.form['shoesize'],
                        request.form['shoeid'],
                        request.form['profileid'])
    elif request.method == 'DELETE':
        return delete_task(request.json['id'])
    else:
        return {'data': 'lol'}


@blueprint.route('/tasks', methods=['GET', 'POST', 'DELETE'])
@login_required
def tasksmanager():
    data = get_all_tasks()
    return render_template('taskmanager.html', tasks=data)


@blueprint.route('/tasks/start', methods=['GET'])
@login_required
def start_tasks():
    data=get_all_tasks()
    return {'msg': str(start_tasks_raffle(data))}
