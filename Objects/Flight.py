import uuid

class Flight:
    def __init__(self, path, drone_id):
        self._id = uuid.uuid4().int
        self._path = path
        self._drone_id = drone_id
        self.time = 0

    def get_id(self):
        return self._id
    
    def set_time(self, time):
        self.time = time

    def get_time(self):
        return self.time
    
    def update_time(self):
        self.time += 1
    