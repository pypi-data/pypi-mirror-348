from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="ExternalResources")


@_attrs_define
class ExternalResources:
    """
    Attributes:
        databases (list[str]):
        indexes (list[str]):
    """

    databases: list[str]
    indexes: list[str]

    def to_dict(self) -> dict[str, Any]:
        databases = self.databases

        indexes = self.indexes

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "databases": databases,
                "indexes": indexes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        databases = cast(list[str], d.pop("databases"))

        indexes = cast(list[str], d.pop("indexes"))

        external_resources = cls(
            databases=databases,
            indexes=indexes,
        )

        return external_resources
