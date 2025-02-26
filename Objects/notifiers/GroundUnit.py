from abc import ABC, abstractmethod

from ..Enums.ForceSide import FroceSide
from ..CombatEntity import CombatEntity


class GroundUnit(CombatEntity, ABC):
    def __init__(self):
        super().__init__(force_side=FroceSide.BLUE)

    @abstractmethod
    def is_coordinate_visible(self, coordinate) -> bool:
        raise NotImplementedError('Not implemented yet')
