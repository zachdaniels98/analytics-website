from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from zdanalytics.db import get_db
from zdanalytics.player_stats import get_pitchers, get_whiffs, get_player_breakdown

bp = Blueprint('baseball', __name__, url_prefix='/baseball')


@bp.route('/')
def home():
    return 'let\'s check'


@bp.route('/player/<int:pid>', methods=('GET',))
def player(pid):
    return get_player_breakdown(pid)


@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        player_id = request.form['player_id']
        error = None

        cursor = get_db().cursor(dictionary=True)
        cursor.execute(
            'SELECT id FROM pitcher WHERE id = %s;', (player_id,)
        )
        if cursor.fetchone() is None:
            error = 'No player with given id.'

        if error is None:
            return redirect(url_for('baseball.player', pid=player_id))
        flash(error)

    return render_template('baseball/search.html')
