from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="VuetifyLightTheme")


@_attrs_define
class VuetifyLightTheme:
    """Standard light colors

    Attributes:
        primary (Union[Unset, str]):  Default: '#1976D2'.
        secondary (Union[Unset, str]):  Default: '#EEEEEE'.
    """

    primary: Union[Unset, str] = "#1976D2"
    secondary: Union[Unset, str] = "#EEEEEE"

    def to_dict(self) -> dict[str, Any]:
        primary = self.primary

        secondary = self.secondary

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if primary is not UNSET:
            field_dict["primary"] = primary
        if secondary is not UNSET:
            field_dict["secondary"] = secondary

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        primary = d.pop("primary", UNSET)

        secondary = d.pop("secondary", UNSET)

        vuetify_light_theme = cls(
            primary=primary,
            secondary=secondary,
        )

        return vuetify_light_theme
