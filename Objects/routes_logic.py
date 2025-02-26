import numpy as np
from geopy.distance import geodesic
import folium
import webbrowser
import os

def get_linear_route(start_coordinate, end_coordinate, v, a, dt=1.0):
    """
      Generates a linear route for a drone given start and end coordinates, initial velocity (v),
      and acceleration (a), using kinematics.

      :param start_coordinate: Tuple (lat, lon) for the start position.
      :param end_coordinate: Tuple (lat, lon) for the end position.
      :param v: Initial velocity (m/s).
      :param a: Acceleration (m/s²).
      :param dt: Time step for calculations (seconds, default 1s).
      :return: List of (lat, lon) coordinates along the route.
    """
    # calculate the distance beetween the 2 coordinate
    total_distance = geodesic(start_coordinate, end_coordinate).meters

    # Solve for time using kinematics equation: d = v*t + 0.5*a*t^2
    roots = np.roots([0.5 * a, v, -total_distance])
    real_roots = roots[roots > 0]
    if len(real_roots) == 0:
        raise ValueError("Cannot reach the destination with given velocity and acceleration.")

    t_final = max(real_roots)  # Get the positive r
    time_steps = np.arange(0, t_final, dt)

    # Final velocity of this segment
    v_end = v + a * t_final

    # calculate the distances with the time stemps:
    distances = v * time_steps + 0.5 * a * time_steps ** 2
    distances = np.clip(distances, 0, total_distance)

    # Compute intermediate coordinates
    route = [start_coordinate]
    for d in distances[1:]:
        fraction = d / total_distance
        lat = start_coordinate[0] + fraction * (end_coordinate[0] - start_coordinate[0])
        lon = start_coordinate[1] + fraction * (end_coordinate[1] - start_coordinate[1])
        route.append((lat, lon))

    return route, v_end


def get_pice_wise_linear_route(coordinates, v0, v_max, accelerations, dt=10.0):
    """
    Generates a full route composed of multiple linear segments, considering velocity continuity.

    :param coordinates: List of (lat, lon) waypoints.
    :param v0: Initial velocity (m/s).
    :param v_max: Maximum  start velocity (m/s).
    :param accelerations: List of acceleration values (m/s²) for each segment.
    :param dt: Time step for calculations (seconds, default 1s).
    :return: List of (lat, lon) coordinates along the full route.
    """
    full_route = []
    # Start with initial velocity
    v = v0

    for i in range(len(coordinates) - 2):
        route_segment, v_end = get_linear_route(coordinates[i], coordinates[i + 1], v, accelerations[i], dt)
        if abs(v_end) >= abs(v_max):
            new_a = (v_max ** 2 - v ** 2) / (2 * geodesic(coordinates[i], coordinates[i + 1]).meters)
            # it is important to note that the time will change because the v will decrease in the next row
            route_segment, v_end = get_linear_route(coordinates[i], coordinates[i + 1], v, new_a, dt)
            v_end = v_max * np.sign(v_end)
            accelerations[i] = new_a
            if np.sign(accelerations[i + 1]) == np.sign(v_end):
                accelerations[i + 1] = 0

        v = v_end

        if full_route:
            full_route.extend(route_segment[1:])  # Avoid duplicating points
        else:
            full_route.extend(route_segment)

    return full_route


def get_circular_route(start_coordinate, end_coordinate, v0, a, vmax, dt=1.0):
    """
    Generates a circular route between two coordinates using a time step (dt).

    :param start_coordinate: Tuple (lat, lon) for the start position.
    :param end_coordinate: Tuple (lat, lon) for the end position.
    :param v0: Initial velocity (m/s).
    :param a: Acceleration (m/s²).
    :param vmax: Maximum velocity (m/s).
    :param dt: Time step for calculations (seconds).
    :return: List of (lat, lon) coordinates along the route.
    """
    center = ((start_coordinate[0] + end_coordinate[0]) / 2, (start_coordinate[1] + end_coordinate[1]) / 2)
    radius = geodesic(start_coordinate, center).meters

    # Calculate the total distance of the circular path (half-circle approximation)
    circumference = 2 * np.pi * radius
    total_time = circumference / vmax  # Time to travel at max velocity

    # Calculate the number of points based on total time and time step
    num_points = int(total_time / dt)

    route = [start_coordinate]
    v = v0
    for i in range(num_points):
        # Determine the angle for the current point
        angle = (np.pi * i) / (num_points - 1)  # Half-circle from 0 to pi

        # Calculate the offsets in latitude and longitude. the 111320 is to convert meters to lat lon offset
        lat_offset = (radius / 111320) * np.cos(angle)
        lon_offset = (radius / (111320 * np.cos(np.radians(center[0])))) * np.sin(angle)

        # Add the point to the route
        route.append((center[0] + lat_offset, center[1] + lon_offset))

        # Update velocity, ensuring it doesn't exceed max velocity
        v = min(max(v + a * dt, 0), vmax)
    v_end = v
    return route, v_end


def plot_route(route,filename):
    """
    Plots the route on a folium map.

    :param route: List of (lat, lon) coordinates along the route.
    """
    m = folium.Map(location=route[0], zoom_start=13)
    folium.PolyLine(route, color='blue', weight=2.5, opacity=1).add_to(m)

    # Add start and end markers
    folium.Marker(route[0], popup="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(route[-1], popup="End", icon=folium.Icon(color='red')).add_to(m)

    filename += ".html"
    m.save(filename)
    webbrowser.open("file://" + os.path.abspath(filename))

    return m


def test_get_linear_route():
    filename = "test_get_linear_route"
    start = (32.0853, 34.7818)  # Tel Aviv
    end = (32.1093, 34.8555)  # Herzliya
    v0 = 10  # m/s
    acceleration = 2  # m/s²

    route, v_end = get_linear_route(start, end, v0, acceleration)
    plot_route(route, filename)

def test_get_pice_wise_linear_route():
    filename = "test_get_pice_wise_linear_route"
    start = (32.0853, 34.7818)  # Tel Aviv
    waypoints = [(32.0950, 34.8000), (32.1093, 34.8555), (32.0853, 34.7818), (32.1093, 34.8555)]  # Intermediate points
    end = (32.1093, 34.8555)  # Herzliya
    coordinates = [start] + waypoints + [end]
    v0 = 10  # m/s
    v_max = 150
    accelerations = [2, 1, 2, 1, 2]  # m/s² for each segment
    full_route = get_pice_wise_linear_route(coordinates, v0, v_max, accelerations)
    plot_route(full_route,filename)

def test_get_circular_route():
    filename = "test_get_circular_route"
    start = (32.0853, 34.7818)  # Tel Aviv
    end = (32.1093, 34.8555)  # Herzliya
    v0 = 10  # m/s
    acceleration = 2  # m/s²
    v_max = 20  # m/s²
    route, v_end = get_circular_route(start, end, v0, acceleration, v_max)
    plot_route(route,filename)

if __name__ == '__main__':
    test_get_linear_route()
    test_get_pice_wise_linear_route()
    test_get_circular_route()