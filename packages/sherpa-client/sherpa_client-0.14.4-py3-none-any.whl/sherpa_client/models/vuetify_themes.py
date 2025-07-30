from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vuetify_dark_theme import VuetifyDarkTheme
    from ..models.vuetify_light_theme import VuetifyLightTheme


T = TypeVar("T", bound="VuetifyThemes")


@attr.s(auto_attribs=True)
class VuetifyThemes:
    """Standard themes

    Attributes:
        dark (Union[Unset, VuetifyDarkTheme]): Standard dark colors
        light (Union[Unset, VuetifyLightTheme]): Standard light colors
    """

    dark: Union[Unset, "VuetifyDarkTheme"] = UNSET
    light: Union[Unset, "VuetifyLightTheme"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        dark: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.dark, Unset):
            dark = self.dark.to_dict()

        light: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.light, Unset):
            light = self.light.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if dark is not UNSET:
            field_dict["dark"] = dark
        if light is not UNSET:
            field_dict["light"] = light

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vuetify_dark_theme import VuetifyDarkTheme
        from ..models.vuetify_light_theme import VuetifyLightTheme

        d = src_dict.copy()
        _dark = d.pop("dark", UNSET)
        dark: Union[Unset, VuetifyDarkTheme]
        if isinstance(_dark, Unset):
            dark = UNSET
        else:
            dark = VuetifyDarkTheme.from_dict(_dark)

        _light = d.pop("light", UNSET)
        light: Union[Unset, VuetifyLightTheme]
        if isinstance(_light, Unset):
            light = UNSET
        else:
            light = VuetifyLightTheme.from_dict(_light)

        vuetify_themes = cls(
            dark=dark,
            light=light,
        )

        return vuetify_themes
