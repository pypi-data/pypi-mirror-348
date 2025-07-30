from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Limit(ABC):
    name: str

    @abstractmethod
    def validate(self, value):
        """RuntimeError :raise if not valid"""


@dataclass
class Enum(Limit):
    values: tuple[int, ...]

    def validate(self, value: int):
        if value not in self.values:
            raise RuntimeError(F"for {self.name} got {value}, expected {self.values}")


@dataclass
class MinMax(Limit):
    min: int
    max: int

    def validate(self, value: int):
        if (
            self.min > value
            or self.max < value
        ):
            raise RuntimeError(F"for {self.name} got {value}, expected ({self.min}..{self.max})")
