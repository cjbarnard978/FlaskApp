import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load the CSV
df = pd.read_csv('saintbirthlocationmap.csv')

# Prepare geocoder
geolocator = Nominatim(user_agent="saint_geocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def build_location(row, prefix):
    parts = []
    if pd.notnull(row[f'{prefix} Location: Specific']):
        parts.append(str(row[f'{prefix} Location: Specific']))
    if pd.notnull(row[f'{prefix} Region']):
        parts.append(str(row[f'{prefix} Region']))
    if pd.notnull(row[f'{prefix} Country']):
        parts.append(str(row[f'{prefix} Country']))
    return ', '.join(parts)

# Create location strings
df['birth_location_query'] = df.apply(lambda row: build_location(row, 'Birth'), axis=1)
df['death_location_query'] = df.apply(lambda row: build_location(row, 'Death'), axis=1)

# Geocode birth locations
birth_latitudes = []
birth_longitudes = []
for loc in df['birth_location_query']:
    if loc.strip() == '' or loc.lower() == 'null':
        birth_latitudes.append(None)
        birth_longitudes.append(None)
        continue
    try:
        location = geocode(loc)
        if location:
            birth_latitudes.append(location.latitude)
            birth_longitudes.append(location.longitude)
        else:
            birth_latitudes.append(None)
            birth_longitudes.append(None)
    except Exception as e:
        birth_latitudes.append(None)
        birth_longitudes.append(None)
        time.sleep(1)

# Geocode death locations
death_latitudes = []
death_longitudes = []
for loc in df['death_location_query']:
    if loc.strip() == '' or loc.lower() == 'null':
        death_latitudes.append(None)
        death_longitudes.append(None)
        continue
    try:
        location = geocode(loc)
        if location:
            death_latitudes.append(location.latitude)
            death_longitudes.append(location.longitude)
        else:
            death_latitudes.append(None)
            death_longitudes.append(None)
    except Exception as e:
        death_latitudes.append(None)
        death_longitudes.append(None)
        time.sleep(1)

# Add results to DataFrame
df['Birth Latitude'] = birth_latitudes
df['Birth Longitude'] = birth_longitudes
df['Death Latitude'] = death_latitudes
df['Death Longitude'] = death_longitudes

# Save to new CSV
df.to_csv('saintbirthlocationmap_geocoded.csv', index=False)
print('Geocoding complete. Results saved to saintbirthlocationmap_geocoded.csv')
