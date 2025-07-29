from typing import (
    Any,
    ClassVar,
    Generic,
    Literal,
    TypeVar,
)

from .base import DBModelMetaclass, RootModel


class InstanceId(RootModel):
    external_id: str
    space: str

    def __hash__(self) -> int:
        return hash((self.external_id, self.space))

    def __eq__(self, other: Any) -> bool:
        return (
            other is not None
            and isinstance(other, InstanceId)
            and self.external_id == other.external_id
            and self.space == other.space
        )

    def as_tuple(self) -> tuple[str, str]:
        return (self.space, self.external_id)


class ViewInstance(InstanceId, metaclass=DBModelMetaclass):
    __view_external_id__: ClassVar[str | None] = None
    __instance_spaces__: ClassVar[list[str] | None] = None
    __instance_spaces_prefix__: ClassVar[str | None] = None

    @classmethod
    def get_view_external_id(cls) -> str:
        return cls.__view_external_id__ or cls.__name__


TViewInstance = TypeVar("TViewInstance", bound=ViewInstance)


class PaginatedResult(RootModel, Generic[TViewInstance]):
    data: list[TViewInstance]
    has_next_page: bool
    next_cursor: str | None


ValidationMode = Literal["raiseOnError", "ignoreOnError"]
