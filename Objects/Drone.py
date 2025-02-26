from .CombatEntity import CombatEntity
from .Enums.ForceSide import FroceSide
from .Flight import Flight
import threading
from time import sleep
from .Path import *

class Drone(CombatEntity):
    def __init__(self, drone_type, current_battery_level, force_side, path):
        super().__init__(force_side)

        self.drone_type = drone_type
        self.current_battery_level = current_battery_level
        self.current_location = 0
        self.is_flying = False
        self.current_flight = None
        self.path = path

    def get_current_location(self):
        return self.current_location

    def get_current_speed(self):
        return self.path.get_current_speed()

    def __str__(self) -> str:
        return f"{self.drone_type.name} location: {str(self.current_location)} speed: {self.get_current_speed()}"

    def update_state(self, wanted_time = None):
        self.current_flight = Flight(self.path, self.id)
        self.current_location = self.path.get_start()
        if wanted_time is None:
            self.is_flying = True
            thread = threading.Thread(target=self.exec_flight, args=(self, ))
            thread.start()
        else:
            self.current_location = self.path.get_current_location(wanted_time)
            self.current_flight.set_time(wanted_time)

    def kill_flight(self):
        self.is_flying = False

    def exec_flight(self):
        while self.is_flying:
            sleep(1)
            self.current_flight.update_time()
            self.current_location = path.get_next_location()
        

        