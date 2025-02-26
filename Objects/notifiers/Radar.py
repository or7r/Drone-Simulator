import math

from haversine import haversine, Unit

from GroundUnit import GroundUnit


class Radar(GroundUnit):
    def __init__(self, coordinate, seeing_distance: float, view_direction, view_angle: float):
        """Radar object for observing drones.

        Args:
            coordinate: (lat, lon) coordinates of the center of the radar
            seeing_distance: The maximum detection range of the radar in METERS.
            view_direction: The azimuth direction the radar is facing in degrees (0° = North, 90° = East).
            view_angle: The field of view of the radar in degrees.

        """
        self.coordinate = coordinate
        self.seeing_distance = seeing_distance
        self.view_direction = view_direction
        self.view_angle = view_angle

    @staticmethod
    def calculate_bearing(coord1, coord2):
        """
        Calculate the bearing (direction) from the first coordinate to the second coordinate.

        Args:
            coord1 (tuple): The starting coordinate as (latitude, longitude) in degrees.
            coord2 (tuple): The target coordinate as (latitude, longitude) in degrees.

        Returns:
            float: The bearing from the first coordinate to the second in degrees (0° = North).
        """
        lat1, lon1 = map(math.radians, coord1)
        lat2, lon2 = map(math.radians, coord2)

        dlon = lon2 - lon1
        x = math.sin(dlon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)

        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)

        return (initial_bearing + 360) % 360  # Normalize to 0-360 degrees

    def is_coordinate_visible(self, target_coord) -> bool:
        """
        Determine if a given geographic coordinate is within the radar's coverage area.

        Args:
            target_coord: The target coordinate as (latitude, longitude) in degrees.

        Returns:
            bool: True if the target is within the radar's coverage, False otherwise.

        """
        distance = haversine(self.coordinate, target_coord, unit=Unit.METERS)
        if distance > self.seeing_distance:
            return False

        bearing = self.calculate_bearing(self.coordinate, target_coord)
        half_view_angle = self.view_angle / 2

        min_angle = (self.view_direction - half_view_angle) % 360
        max_angle = (self.view_direction + half_view_angle) % 360

        if min_angle < max_angle:
            in_angle = min_angle <= bearing <= max_angle
        else:
            in_angle = bearing >= min_angle or bearing <= max_angle

        return in_angle

