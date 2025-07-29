from abc import ABC, abstractmethod
from typing import List


class IMemory(ABC):
    @property
    def memory_count(self) -> int:
        pass

    @abstractmethod
    def get_memory_type(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_module_type(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_size_in_GB(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_speed(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_rank(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_voltage(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_bank(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_manufacturing_date_code(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_temperature(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_write_protection(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_module_manufacture(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_manufacture(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_part_number(self, memory_number: int) -> str:
        pass

    @abstractmethod
    def get_memory_specific(self, memory_number: int) -> str:
        pass
