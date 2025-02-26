class CombatEntity:
    entity_counter = 0

    def __init__(self, force_side):
        self.force_side = force_side
        self.id = CombatEntity.entity_counter
        CombatEntity.entity_counter += 1

    def get_id(self):
        return self.id

    def get_current_state(self):
        pass