import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load the CSV
df = pd.read_csv('SaintBirths.csv')

# Prepare geocoder
geolocator = Nominatim(user_agent="saint_geocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Geocode Birth Region
latitudes = []
longitudes = []
for region in df['Birth Region']:
    if pd.isnull(region) or str(region).strip() == '' or str(region).lower() == 'null':
        latitudes.append(None)
        longitudes.append(None)
        continue
    try:
        location = geocode(region)
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
df['Birth Region Latitude'] = latitudes
df['Birth Region Longitude'] = longitudes

# Save to new CSV
df.to_csv('SaintBirths_geocoded.csv', index=False)
print('Geocoding complete. Results saved to SaintBirths_geocoded.csv')
