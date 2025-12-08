import pandas as pd
import plotly.graph_objects as go

# Load data
saints = pd.read_csv('SaintBirths.csv')

fig = go.Figure()

for _, row in saints.iterrows():
    # Check for valid coordinates
    if pd.notna(row['Birth_Latitude']) and pd.notna(row['Death_Latitude']) and pd.notna(row['Birth_ Longitude']) and pd.notna(row['Death_Longitude']):
        fig.add_trace(go.Scattermapbox(
            mode = "lines",
            lon = [float(row['Birth_ Longitude']), float(row['Death_Longitude'])],
            lat = [float(row['Birth_Latitude']), float(row['Death_Latitude'])],
            line = dict(width=2, color='blue'),
            name = row['Saint']
        ))

fig.update_layout(
    mapbox = dict(
        style = "open-street-map",
        center = dict(lat=54, lon=-3),
        zoom = 4
    ),
    showlegend = True,
    title = "Saints' Birth to Death Locations"
)

fig.show()
