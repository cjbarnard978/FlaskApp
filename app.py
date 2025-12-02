from flask import Flask, render_template
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    return ('hello world')

import plotly.graph_objects as go
import pandas as pd
df = pd.read_csv('interactivemonasterymap.csv')
Latitude = df.lat 
Longitude = df.lon
'Monastery,' 'Monastery Type,' 'Date founded,' 'Founder,' 'Current Status' = df.text
fig = go.Figure()
fig.add_trace(go.Scattermap(
    lat=Latitude,
    lon=Longitude,
    mode='marker',
    marker=go.scattermap.Marker(
        size=17
        color='blue'
        opacity=0.7
    ),
    text='Monastery,' 'Monastery Type,' 'Date founded,' 'Founder,' 'Current Status'
))
fig.update_layout(
    title=dict(text='Medieval Monasteries of the Bannatyne Club'),
    autosize=True,
    hovermod='closest',
    showlegend=False,
    map=dict(
        bearing=0,
        center=dict(
            lat=55.9523
            lon=3.1882
        ),
        pitch=0,
        zoom=5,
        style='topo'
    ),
)
fig.show()