import json

# Load GB and IRE geojson files
with open('GBgeojson.geojson', 'r') as gb_file:
    gb_geojson = json.load(gb_file)
with open('IREgeojson.geojson', 'r') as ire_file:
    ire_geojson = json.load(ire_file)

# Combine features
combined_features = gb_geojson['features'] + ire_geojson['features']

# Create new combined geojson
combined_geojson = {
    "type": "FeatureCollection",
    "features": combined_features
}

# Save to new file in geojson folder
import os
os.makedirs('geojson', exist_ok=True)
with open('geojson/combined_british_isles.geojson', 'w') as out_file:
    json.dump(combined_geojson, out_file)

print('Combined GeoJSON saved to geojson/combined_british_isles.geojson')
