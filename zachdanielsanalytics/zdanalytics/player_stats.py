import pandas as pd
from sqlalchemy import create_engine
import json
from zdanalytics.db import get_db
from flask import jsonify

df = None


def get_pitchers():
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('SELECT * FROM pitcher;')
    pitchers = cursor.fetchall()
    return json.dumps(pitchers)


def get_player_stats(player_id, return_json=False):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        'SELECT pitch_type, player_name, pitcher, events, description, zone, des, stand, p_throws, type, at_bat_number'
        ' FROM pitches'
        ' WHERE pitcher = %s;',
        (player_id,))
    stats = cursor.fetchall()
    global df
    df = pd.read_json(json.dumps(stats), orient='records')
    if return_json:
        return json.dumps(stats)


def get_player_breakdown(player_id):
    get_player_stats(player_id)
    breakdown = {
        'pitch_breakdown': get_pitch_breakdown(),
        'whiff': get_whiffs(),
        'zone_distribution': get_pitch_by_zone(),
        'batting_avg': get_opp_ba()
    }
    return jsonify(breakdown)


def get_pitch_breakdown():
    by_type = df[['pitch_type', 'type']].groupby('pitch_type').count()
    by_type['pitch_type'] = by_type.pop('type')
    return by_type.to_dict()


def get_whiffs():
    miss = ['missed_bunt', 'swinging_strike', 'swinging_strike_blocked']
    swings = df[df['type'].isin(['S', 'X'])]
    missed = swings[swings['description'].isin(miss)]
    whiff_pct = len(missed.index) / len(swings.index)
    whiff_pct_by_pitch = (
            missed[['pitch_type', 'type']].groupby('pitch_type').count() /
            swings[['pitch_type', 'type']].groupby('pitch_type').count()
    )
    whiff = {'overall_pct': round(whiff_pct, 3)}
    whiff.update(whiff_pct_by_pitch.round(3).to_dict())
    whiff['pct_by_pitch'] = whiff.pop('type')
    return whiff


def get_pitch_by_zone():
    by_zone = df[['type', 'zone']].groupby('zone').count()
    by_zone.index = by_zone.index.astype('int64')
    by_zone['zone'] = by_zone.pop('type')
    return by_zone.to_dict()


def get_opp_ba():
    out = ['double_play', 'field_error', 'field_out', 'fielders_choice', 'fielders_choice_out', 'force_out',
           'grounded_into_double_play', 'strikeout']
    hit = ['single', 'double', 'triple', 'home_run']
    at_bat = out + hit
    all_ab = df[df['events'].isin(at_bat)][['events', 'stand']]
    results = all_ab.groupby('events').count()
    all_hits = results.reindex(hit)
    opp_ba = all_hits.sum() / results.sum()
    left_ab = all_ab[all_ab['stand'] == 'L'].groupby('events').count()
    left_hits = left_ab.reindex(hit)
    right_ab = all_ab[all_ab['stand'] == 'R'].groupby('events').count()
    right_hits = right_ab.reindex(hit)
    opp_ba_left = left_hits.sum() / left_ab.sum()
    opp_ba_right = right_hits.sum() / right_ab.sum()
    ba = {'opp_ba': opp_ba.round(3).array[0]}
    ba.update({
        'opp_ba_left': opp_ba_left.round(3).array[0],
        'opp_ba_right': opp_ba_right.round(3).array[0]
    })
    return ba

