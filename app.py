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
monastery_info = df.text
fig = go.Figure()
fig.add_trace(go.Scattermapbox(
    lat=Latitude,
    lon=Longitude,
    mode='markers',
    marker=dict(
        size=17,
        color='blue',
        opacity=0.7
    ),
    text=monastery_info
))
fig.update_layout(
    title='Medieval Monasteries of the Bannatyne Club',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        bearing=0,
        center=dict(
            lat=55.9523,
            lon=3.1882
        ),
        pitch=0,
        zoom=5,
        style='open-street-map'
    ),
)
fig.show()
if __name__ == '__main__':
    app.run(debug=True)