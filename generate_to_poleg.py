import random
import sys
import uuid
from enum import Enum

import arrow
import geopandas as gpd
from faker import Faker
from shapely.geometry import Point

GEOJSON = "C:/Users/adari/Documents/Drone-Simulator/israel.json"

def random_coordinate_in_geojson_gpd() -> tuple:
  """
  Generate a random coordinate inside a GeoJSON object using GeoPandas.

  Parameters:
  - geojson_data: The GeoJSON data as a dictionary.

  Returns:
  - A tuple containing the latitude and longitude.
  """
  try:
    # Convert GeoJSON to GeoDataFrame
    gdf = gpd.read_file(GEOJSON)

    # Get the bounds of the geometry
    minx, miny, maxx, maxy = gdf.geometry.total_bounds

    # Generate random points until one is inside the geometry
    while True:
      pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
      if gdf.geometry.contains(pnt).any():
        return float(pnt.y), float(pnt.x)
  except Exception as e:
    print(f"An error occurred: {e}")

class DroneClassification(Enum):
  Recognized = 1,
  Unrecognized = 2,
  Enemy = 3,


def generate_drone():
  id = int(uuid.uuid4().hex, 16)
  name = Faker().word()
  battery = random.randint(0,100)
  speed = random.uniform(0, 100)
  video = "OK" if random.choice([True, False]) else "BAD"

  return {"id": id, "name": name, "battery": battery, "speed": speed, "video": video}

def generate_location():
  id = int(uuid.uuid4().hex, 16)
  drone_id = int(uuid.uuid4().hex, 16)
  lat, lon = random_coordinate_in_geojson_gpd()
  timestamp = arrow.now()
  image = "OK" if random.choice([True, False]) else "BAD"
  flight = random.randint(0,100)

  return {"id": id, "drone_id": drone_id, "lat": lat, "lon": lon, "timestamp": timestamp, "image": image, "flight": flight}


sys.stdout.write(str(generate_location()))