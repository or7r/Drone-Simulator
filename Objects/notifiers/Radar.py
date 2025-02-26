import math

import folium
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
        super().__init__()
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
        # Check the distance to the target
        distance = haversine(self.coordinate, target_coord, unit=Unit.METERS)
        if distance > self.seeing_distance:
            return False

        # Check if the target is within the radar's angular field of view
        bearing = self.calculate_bearing(self.coordinate, target_coord)
        half_view_angle = self.view_angle / 2

        # Calculate the angular range the radar covers
        min_angle = (self.view_direction - half_view_angle) % 360
        max_angle = (self.view_direction + half_view_angle) % 360

        # Check if the bearing of the target is within the angular range
        if min_angle < max_angle:
            in_angle = min_angle <= bearing <= max_angle
        else:
            in_angle = bearing >= min_angle or bearing <= max_angle

        return in_angle

    def point_in_radius(self, angle, distance):
        """
        Calculate the target point at a certain distance and angle from the radar position.
        """
        lat1, lon1 = map(math.radians, self.coordinate)

        # Earth's radius in meters
        R = 6371000  # meters

        # Convert distance from meters to radians
        lat_dist = distance / R
        lon_dist = distance / (R * math.cos(lat1))

        # Calculate the new point using the bearing (angle)
        target_lat = lat1 + lat_dist * math.cos(math.radians(angle))
        target_lon = lon1 + lon_dist * math.sin(math.radians(angle))

        return math.degrees(target_lat), math.degrees(target_lon)

    def plot_coverage(self, map_obj):
        """
        Plot the radar's coverage area as a slice of a circle (sector) on the given folium map.
        """
        # Plot radar position as a marker
        folium.Marker(
            location=self.coordinate,
            popup="Radar Coverage",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(map_obj)

        # Calculate the boundary points of the sector
        half_view_angle = self.view_angle / 2

        # Calculate the two extreme angles
        start_angle = int((self.view_direction - half_view_angle) % 360)
        end_angle = int((self.view_direction + half_view_angle) % 360)

        # If the start angle is greater than the end angle, we need to handle the wraparound
        if start_angle > end_angle:
            # Two parts: one from start_angle to 360 and one from 0 to end_angle
            angles_1 = range(start_angle, 360)
            angles_2 = range(0, end_angle + 1)
            angles = list(angles_1) + list(angles_2)
        else:
            # Single part: from start_angle to end_angle
            angles = range(start_angle, end_angle + 1)

        # Create points around the boundary of the sector
        points = [self.coordinate]

        # Generate the boundary points of the sector
        for angle in angles:
            target_point = self.point_in_radius(angle, self.seeing_distance)
            points.append(target_point)

        # Close the polygon by adding the first point again
        points.append(self.coordinate)

        # Plot the sector as a polygon (slice of a circle)
        folium.Polygon(
            locations=points,
            color='blue',
            fill=True,
            fill_opacity=0.2
        ).add_to(map_obj)

        # Optionally, add the view direction line (to help visualize the center)
        end_lat, end_lon = self.point_in_radius(self.view_direction, self.seeing_distance)
        folium.Marker(
            location=(end_lat, end_lon),
            icon=folium.Icon(color='red', icon='arrow-right')
        ).add_to(map_obj)
