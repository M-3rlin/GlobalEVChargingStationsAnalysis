from global_land_mask import globe
import random
import pandas as pd

# Read your data
df = pd.read_csv("stations.csv")

# City bounding boxes
city_boxes = {
    "Houston": {
        "lat": (29.5, 30.1),
        "lon": (-95.8, -95.0),
    },
    "San Francisco": {
        "lat": (37.70, 37.82),
        "lon": (-122.52, -122.36),
    },
    "Los Angeles": {
        "lat": (33.70, 34.35),
        "lon": (-118.67, -118.16),
    },
    "Chicago": {
        "lat": (41.64, 42.05),
        "lon": (-87.94, -87.52),
    },
    "New York": {
        "lat": (40.49, 40.92),
        "lon": (-74.27, -73.68),
    },
}

# Optional: seed for reproducibility
rng = random.Random(42)

def generate_land_coord_for_city(city, max_tries=1000):
    """
    Generate a random (lat, lon) inside the bounding box for `city`,
    retrying until it lands on land or max_tries is exceeded.
    """
    if city not in city_boxes:
        return float("nan"), float("nan")
    
    lat_min, lat_max = city_boxes[city]["lat"]
    lon_min, lon_max = city_boxes[city]["lon"]
    
    for _ in range(max_tries):
        lat = rng.uniform(lat_min, lat_max)
        lon = rng.uniform(lon_min, lon_max)
        
        # Only accept if on land
        if globe.is_land(lat, lon):
            return lat, lon
    
    # If we fail too many times, give up with NaNs (or relax constraints)
    return float("nan"), float("nan")

# Generate one coordinate pair per unique station_id
coords_by_station = {}

for station_id, city in (
    df[["station_id", "Charging Station Location"]]
    .drop_duplicates()
    .itertuples(index=False)
):
    lat, lon = generate_land_coord_for_city(city)
    coords_by_station[station_id] = (lat, lon)

# Map back to the dataframe
df["lat"] = df["station_id"].map(lambda sid: coords_by_station[sid][0])
df["lon"] = df["station_id"].map(lambda sid: coords_by_station[sid][1])

# Save result
df.to_csv("stations_with_land_only_coords.csv", index=False)
