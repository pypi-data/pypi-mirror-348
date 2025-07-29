from abc import ABC, abstractmethod


class IDisk(ABC):
    @property
    @abstractmethod
    def total_disk_space(self) -> int:
        pass

    @property
    @abstractmethod
    def free_disk_space(self) -> int:
        pass
