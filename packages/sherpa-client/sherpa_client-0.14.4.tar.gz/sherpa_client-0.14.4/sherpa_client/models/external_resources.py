from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="ExternalResources")


@attr.s(auto_attribs=True)
class ExternalResources:
    """
    Attributes:
        databases (List[str]):
        indexes (List[str]):
    """

    databases: List[str]
    indexes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        databases = self.databases

        indexes = self.indexes

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "databases": databases,
                "indexes": indexes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        databases = cast(List[str], d.pop("databases"))

        indexes = cast(List[str], d.pop("indexes"))

        external_resources = cls(
            databases=databases,
            indexes=indexes,
        )

        return external_resources
