from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from zdanalytics.player_stats import get_pitchers

bp = Blueprint('baseball', __name__, url_prefix='/baseball')


@bp.route('/')
def home():
    return 'home'


@bp.route('/player', methods=('GET', 'POST'))
def player():
    return get_pitchers()
