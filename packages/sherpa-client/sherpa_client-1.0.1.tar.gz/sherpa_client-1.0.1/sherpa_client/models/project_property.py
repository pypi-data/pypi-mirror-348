from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectProperty")


@_attrs_define
class ProjectProperty:
    """
    Attributes:
        name (Union[Unset, str]):  Default: 'value'.
    """

    name: Union[Unset, str] = "value"

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        project_property = cls(
            name=name,
        )

        return project_property
