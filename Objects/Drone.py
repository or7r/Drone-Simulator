from .CombatEntity import CombatEntity
from .Enums.ForceSide import FroceSide

class Drone(CombatEntity):
    def __init__(self, drone_type, current_location, current_speed, current_battery_level):
        self.drone_type = drone_type
        self.current_location = current_location
        self.current_speed = current_speed
        self.current_battery_level = current_battery_level

    def __str__(self) -> str:
        return f"{self.drone_type.name} location: {str(self.current_location)} speed: {self.current_speed}"

    def update_state():
        pass