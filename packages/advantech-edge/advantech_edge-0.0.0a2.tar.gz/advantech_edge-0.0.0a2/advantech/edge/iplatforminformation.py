from abc import ABC, abstractmethod

class IPlatformInformation(ABC):
    
    @property
    @abstractmethod
    def motherboard_name(self) -> str:
        pass

    @property
    @abstractmethod
    def bios_revision(self) -> str:
        pass
