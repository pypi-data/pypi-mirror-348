from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="ExternalDatabases")


@_attrs_define
class ExternalDatabases:
    """
    Attributes:
        databases (list[str]):
    """

    databases: list[str]

    def to_dict(self) -> dict[str, Any]:
        databases = self.databases

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "databases": databases,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        databases = cast(list[str], d.pop("databases"))

        external_databases = cls(
            databases=databases,
        )

        return external_databases
