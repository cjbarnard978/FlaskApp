from flask import Flask, render_template, jsonify
import csv
import os 
import _sqlite3

app = Flask(__name__)

from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['scotsirishsaints.db'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)