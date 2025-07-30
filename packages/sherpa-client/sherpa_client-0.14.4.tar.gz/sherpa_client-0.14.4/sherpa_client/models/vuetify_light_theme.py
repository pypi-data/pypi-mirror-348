from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="VuetifyLightTheme")


@attr.s(auto_attribs=True)
class VuetifyLightTheme:
    """Standard light colors

    Attributes:
        primary (Union[Unset, str]):  Default: '#1976D2'.
        secondary (Union[Unset, str]):  Default: '#EEEEEE'.
    """

    primary: Union[Unset, str] = "#1976D2"
    secondary: Union[Unset, str] = "#EEEEEE"

    def to_dict(self) -> Dict[str, Any]:
        primary = self.primary
        secondary = self.secondary

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if primary is not UNSET:
            field_dict["primary"] = primary
        if secondary is not UNSET:
            field_dict["secondary"] = secondary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        primary = d.pop("primary", UNSET)

        secondary = d.pop("secondary", UNSET)

        vuetify_light_theme = cls(
            primary=primary,
            secondary=secondary,
        )

        return vuetify_light_theme
