from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="LabelNames")


@_attrs_define
class LabelNames:
    """
    Attributes:
        names (Union[Unset, list[str]]):
    """

    names: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.names, Unset):
            names = self.names

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if names is not UNSET:
            field_dict["names"] = names

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        names = cast(list[str], d.pop("names", UNSET))

        label_names = cls(
            names=names,
        )

        return label_names
