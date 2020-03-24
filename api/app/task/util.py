from flask import session
from app.base.models import User
from flask_login import current_user
import json
from app import db
# from app.raffle.util import RaffleCheckout

from app.raffle.util import RaffleCheckout as rc


def get_all_tasks():
    user = User.query.filter_by(username=current_user.username).first()
    try:
        data = json.loads(user.tasks)
    except:
        data = {
            'tasks': []
        }

    return data


def add_task(sites, name, link, entries, size, shoeid, profileid):
    user = User.query.filter_by(username=current_user.username).first()
    try:
        data = json.loads(user.tasks)
    except:
        data = {
            'tasks': []
        }

    data_profile = json.loads(user.profiles)

    if profileid == 'add':
        for profile in data_profile['data']:
            id = len(data['tasks']) + 1
            link = link
            data['tasks'].append({'id': id,
                                  'sites': sites,
                                  'shoeid': shoeid,
                                  'link': link,
                                  'name': name,
                                  'entries': entries,
                                  'size': size,
                                  'profileid': profile['id']})
    else:
        id = len(data['tasks']) + 1
        link = link
        data['tasks'].append({'id': id,
                              'sites': sites,
                              'shoeid': shoeid,
                              'link': link,
                              'name': name,
                              'entries': entries,
                              'size': size,
                              'profileid': profileid})
    datajson = json.dumps(data)
    setattr(user, 'tasks', datajson)
    db.session.commit()
    return {'taskid': id, 'msg': ' Raffle added to the tasks'}, 201


def delete_task(taskid):
    user = User.query.filter_by(username=current_user.username).first()
    data = json.loads(user.tasks)
    filtered_task = []
    for task in data['tasks']:
        if int(task['id']) == int(taskid):
            print('deleted')
            continue
        filtered_task.append(task)
    filtered_task_json = {
        "tasks": filtered_task
    }
    datajson = json.dumps(filtered_task_json)
    user = User.query.filter_by(username=current_user.username).first()
    setattr(user, 'tasks', datajson)
    db.session.commit()
    return "deleted"


def start_tasks_raffle(tasks):
    # Delete tasks
    # user = User.query.filter_by(username=current_user.username).first()
    # setattr(user, 'tasks', None)
    # db.session.commit()
    # Iterate through tasks
    raffle = rc(tasks)
    raffle.run()
    return {'msg': 'running'}
