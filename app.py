from flask import Flask, render_template
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    return ('hello world')

@app.route('/monasteries')
def monasteries():
    import plotly.io as pio
    plot_html = pio.to_html(fig, full_html=False)
    return render_template('monasteries.html', plot_html=plot_html)

import plotly.graph_objects as go
import pandas as pd
df = pd.read_csv('interactivemonasterymap.csv')
Latitude = df['Latitude']
Longitude = df['Longitude']
monastery_info = df[['Monastery', 'Monastery Type', 'Date founded', 'Founder', 'Current Status']]
hover_text = monastery_info.apply(lambda row: f"Monastery: {row['Monastery']}<br>Type: {row['Monastery Type']}<br>Date Founded: {row['Date founded']}<br>Founder: {row['Founder']}<br>Status: {row['Current Status']}", axis=1)
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
    text=hover_text,
    hoverinfo='text'
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
            lon=-3.1882
        ),
        pitch=0,
        zoom=5,
        style='open-street-map'
    ),
)

if __name__ == '__main__':
    app.run(debug=True)