
from flask import Flask
from flask import g 
import sqlite3
import plotly 
app = Flask(__name__)

DATABASE = '/FlaskApp/scotsirishsaints.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db 
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
@app.route('/localhost:5001/')
def index():
    cur = get_db().cursor()
    
CSV_FILE = 'GaelicIrelandDataFinal.csv'


