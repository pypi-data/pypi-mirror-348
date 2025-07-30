from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="ExternalDatabases")


@attr.s(auto_attribs=True)
class ExternalDatabases:
    """
    Attributes:
        databases (List[str]):
    """

    databases: List[str]

    def to_dict(self) -> Dict[str, Any]:
        databases = self.databases

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "databases": databases,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        databases = cast(List[str], d.pop("databases"))

        external_databases = cls(
            databases=databases,
        )

        return external_databases
