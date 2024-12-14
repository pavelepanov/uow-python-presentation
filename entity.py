from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar('T')


@dataclass(eq=False)
class Entity(ABC, Generic[T]):
    id_: T

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and other.id_ == self.id_

    def __hash__(self) -> int:
        return hash(self.id_)


@dataclass(frozen=True, repr=False)
class UserId:
    value: int


@dataclass(eq=False, kw_only=True)
class User(Entity[UserId]):
    name: str
