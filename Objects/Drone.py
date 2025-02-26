from Entity import CombatEntity 
from Enums.ForceSide import FroceSide
class Drone(CombatEntity):
    def __init__(self, drone_type, current_location, current_speed, current_battery_level):
        self.drone_type = drone_type
        self.current_location = current_location
        self.current_speed = current_speed
        self.current_battery_level = current_battery_level

    def __str__(self) -> str:
        show_str = "RED" if self.drone_type == FroceSide.RED else "BLUE"
        show_str += f" {str(self.current_location)} {self.current_speed}"

    def update_state():
        pass