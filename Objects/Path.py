from .routes_logic import *
import random

class Path:
    def __init__(self, start, end):
        self.routes = get_linear_route(start, end, 10, 2)
        self.num_of_route = 0
    
    def get_start(self):
        return self.routes[0]
    
    def get_next_point(self):
        self.num_of_route += 1
        return self.routes[self.num_of_route]
    
    def get_current_speed(self):
        return self.num_of_route * 2 + 10

    def get_current_location(self, time):
        return self.routes[time] 