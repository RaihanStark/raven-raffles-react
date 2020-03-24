from app.raffle import blueprint
from requests_html import HTMLSession
from app.raffle.models import Shoes
from app import db
from .util import RaffleSpider, get_all_raffles, get_raffle_by_id, RaffleCheckout, refresh_raffles
from flask import request, session, render_template, url_for, redirect


@blueprint.route('/raffles/<int:id>')
def shoes(id):
    raffle = get_raffle_by_id(id)
    return render_template('raffle-shoes.html', raffle=raffle)


@blueprint.route('/v1/refresh')
def refreshraffle():
    refresh_raffles()
    return {'msg': 'done'}


@blueprint.route('/raffles/run', methods=['POST'])
def runraffles():
    if request.method == 'POST':
        tasks = request.json['tasks']
        RaffleCheckout(tasks)
        return {'msg': tasks}
