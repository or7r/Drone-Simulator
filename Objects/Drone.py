from .CombatEntity import CombatEntity
from .Enums.ForceSide import FroceSide
import Flight

class Drone(CombatEntity):
    def __init__(self, drone_type, current_battery_level, force_side):
        super(force_side)

        self.drone_type = drone_type
        self.current_battery_level = current_battery_level
        self.is_flying = False

    def get_current_location():
        pass

    def get_current_speed():
        pass

    def __str__(self) -> str:
        return f"{self.drone_type.name} location: {str(self.current_location)} speed: {self.current_speed}"

    def update_state():
        pass

    def exec_flight():
        pass