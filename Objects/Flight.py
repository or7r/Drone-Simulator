import uuid

class Flight:
    def __init__(self, path, drone_id):
        self._id = uuid.uuid4().int
        self._path = path
        self._drone_id = drone_id

    @getattr
    def get_id(self):
        return self._id