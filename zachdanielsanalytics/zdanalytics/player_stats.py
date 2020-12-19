import pandas as pd
import numpy as np
import math
from pybaseball import playerid_reverse_lookup
from sqlalchemy import create_engine
import json
from zdanalytics.db import get_db


def db_connect(player_id):
    # engine = create_engine('mysql+mysqlconnector://zachdaniels98:Password123@localhost:3306/baseball')
    # cxn = engine.connect()
    # query = '''SELECT pitch_type, player_name, pitcher, events, description, zone, des, stand, p_throws,
    # type, at_bat_number
    #         FROM pitches
    #         WHERE pitcher = ''' + player_id + ''';'''
    # pitch_chunks = pd.read_sql(sql=query, con=cxn, chunksize=1000)
    # cxn.close()
    # pitch_data = pd.concat(pitch_chunks)
    # pitch_data.reset_index(inplace=True)
    # by_pitch_clean = pitch_data.dropna(subset=['pitch_type'])
    # arsenal, pitch_counts = np.unique(np.asarray(by_pitch_clean['pitch_type']), return_counts=True)
    # arsenal = np.array2string(arsenal)
    # pitch_counts = np.array2string(pitch_counts)
    # return arsenal, pitch_counts
    cursor = get_db().cursor(dictionary=True)
    cursor.execute('SELECT * FROM pitcher;')
    pitchers = cursor.fetchall()
    return json.dumps(pitchers)

# def get_pitches_thrown():
#
#
# def get_pitch_counts():
#
#
# def get_whiff_pct():
#
#
# def get_whiff_by_pitch():
#
#
# def get_pitch_by_zone():
#
#
# def get_opp_ba():
#
#
# def get_opp_ba_handed():
