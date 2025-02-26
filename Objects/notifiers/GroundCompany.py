import folium
from haversine import haversine, Unit

from .GroundUnit import GroundUnit


class GroundCompany(GroundUnit):

    def __init__(self, coordinate, seeing_distance: float):
        """Ground forces object for observing drones.

        Args:
            coordinate: (lat, lon) coordinates of the center of the radar
            seeing_distance: The maximum detection range radius of the troops in METERS.

        """
        super().__init__()
        self.coordinate = coordinate
        self.seeing_distance = seeing_distance

    def is_coordinate_visible(self, target_coord) -> bool:
        """
        Determine if a given geographic coordinate is within the troop's observation range.

        Args:
            target_coord: The target coordinate as (latitude, longitude) in degrees.

        Returns:
            bool: True if the target is within the troop's observation range, False otherwise.
        """
        # Calculate the distance between the troop and the target using the haversine method
        distance = haversine(self.coordinate, target_coord, unit=Unit.METERS)

        # If the distance is within the troop's seeing distance, it's visible
        return distance <= self.seeing_distance

    def plot_coverage(self, map_obj):
        """
        Plot the troop's observation range as a circle on the given folium map.
        """
        # Plot troop position as a marker
        folium.Marker(
            location=self.coordinate,
            popup="Troop Position",
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(map_obj)

        # Plot the coverage area as a circle with the troop's seeing distance
        folium.Circle(
            location=self.coordinate,
            radius=self.seeing_distance,
            color='blue',
            fill=True,
            fill_opacity=0.2
        ).add_to(map_obj)
