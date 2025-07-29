from abc import ABC, abstractmethod
from typing import List
from enum import Enum


class GpioDirectionType(Enum):
    INPUT = 0
    OUTPUT = 1


class GpioLevelType(Enum):
    LOW = 0
    HIGH = 1


class InputLevelChangedEventTypes(Enum):
    RisingEdge = 0
    FallingEdge = 1


class IGpio(ABC):
    @abstractmethod
    def get_direction(self, pin: str) -> None:
        pass

    @abstractmethod
    def set_direction(self, pin: str, direction: GpioDirectionType) -> None:
        pass

    @abstractmethod
    def get_level(self, pin: str) -> None:
        pass

    @abstractmethod
    def set_level(self, pin: str, level: GpioLevelType) -> None:
        pass

    # @property
    # @abstractmethod
    # def pins(self) -> List[str]:
    #     pass
