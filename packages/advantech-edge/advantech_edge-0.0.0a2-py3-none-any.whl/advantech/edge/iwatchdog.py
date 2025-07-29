from abc import ABC, abstractmethod
from typing import List


class IWatchDog(ABC):
    @abstractmethod
    def start_timer(self, timer: str, delay: int, event_timeout: int, reset_timeout: int) -> None:
        pass

    @abstractmethod
    def stop_timer(self, timer: str) -> None:
        pass

    @abstractmethod
    def trigger_timer(self, timer: str) -> None:
        pass

    @abstractmethod
    def timer_timeout(self, timer: str) -> None:
        pass
        # todo

    @abstractmethod
    @property
    def timers(self) -> List[str]:
        pass
