from abc import ABC

class CombatEntity(ABC):
    entity_counter = 0

    def __init__(self, force_side):
        self.force_side = force_side
        self.id = entity_counter
        entity_counter += 1

    def get_id(self):
        return self.id

    def get_current_state():
        pass