from flask import current_app, g
import mysql.connector


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(user='zachdaniels98', password='Password123',
                                      host='localhost', database='baseball')
        # cursor = g.db.cursor(dictionary=True)
        # cursor.execute("SELECT * FROM pitcher;")
        # pitchers = cursor.fetchall()
        # print(pitchers)

    return g.db
