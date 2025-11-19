
from flask import Flask, render_template 
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

CSV = 'GaelicIrelandDataFinal.csv'


CSV = "saints.csv"
import plotly.express as px
app.route('/')
render_template('visualization.html')
df = px.data.gapminder().query("SaintID=='Name'")
fig = px.line(df, x="Name", y="Death_date", title='Death Date of Irish and Scottish Saints')
fig.show()


