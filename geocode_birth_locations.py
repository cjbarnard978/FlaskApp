import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load the CSV
df = pd.read_csv('saintbirthlocationmap.csv')

# Prepare geocoder
geolocator = Nominatim(user_agent="saint_geocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def build_location(row):
    parts = []
    if pd.notnull(row['Birth Location: Specific']):
        parts.append(str(row['Birth Location: Specific']))
    if pd.notnull(row['Birth Region']):
        parts.append(str(row['Birth Region']))
    if pd.notnull(row['Birth Country']):
        parts.append(str(row['Birth Country']))
    return ', '.join(parts)

# Create location strings
df['birth_location_query'] = df.apply(build_location, axis=1)

# Geocode
latitudes = []
longitudes = []
for loc in df['birth_location_query']:
    if loc.strip() == '' or loc.lower() == 'null':
        latitudes.append(None)
        longitudes.append(None)
        continue
    try:
        location = geocode(loc)
        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)
    except Exception as e:
        latitudes.append(None)
        longitudes.append(None)
        time.sleep(1)

# Add results to DataFrame
df['Birth Latitude'] = latitudes
df['Birth Longitude'] = longitudes

# Save to new CSV
df.to_csv('saintbirthlocationmap_geocoded.csv', index=False)
print('Geocoding complete. Results saved to saintbirthlocationmap_geocoded.csv')
