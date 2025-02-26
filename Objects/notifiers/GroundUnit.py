from abc import ABC, abstractmethod

from ..Entity import CombatEntity


class GroundUnit(CombatEntity, ABC):
    @abstractmethod
    def is_coordinate_visible(self, coordinate) -> bool:
        raise NotImplementedError('Not implemented yet')
