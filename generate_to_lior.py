import random
import sys
import time
from enum import Enum
from uuid import uuid1, getnode

import geopandas as gpd
from faker import Faker
from shapely.geometry import Point

GEOJSON = "C:/Users/adari/Documents/Drone-Simulator/israel.json"

class DroneClassification(Enum):
  Recognized = 1,
  Unrecognized = 2,
  Enemy = 3,

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

def generate_random_string_with_words(num_words: int = 5) -> str:
  """
  Generate a random string with words.

  Parameters:
  - num_words: The number of words to include in the string. Default is 5.

  Returns:
  - A string containing random words.
  """
  fake = Faker()
  words = [fake.word() for _ in range(num_words)]
  return ' '.join(words)

_my_clock_seq = random.getrandbits(14)
_my_node = getnode()

uuid = str(uuid1(node=_my_node, clock_seq=_my_clock_seq)).replace("-", "")[:16]

lat, lon = random_coordinate_in_geojson_gpd()

classification = random.randint(1,3)

x = {'id': uuid, 'classification': classification, 'lat': lat, 'lon': lon, 'description': generate_random_string_with_words(), 'creation_time': time.time()}

sys.stdout.write(str(x).replace("'", '"'))