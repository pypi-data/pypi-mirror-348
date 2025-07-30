from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vuetify_themes import VuetifyThemes


T = TypeVar("T", bound="VuetifyConfig")


@attr.s(auto_attribs=True)
class VuetifyConfig:
    """Standard configuration

    Attributes:
        dark (Union[Unset, bool]):
        themes (Union[Unset, VuetifyThemes]): Standard themes
    """

    dark: Union[Unset, bool] = False
    themes: Union[Unset, "VuetifyThemes"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        dark = self.dark
        themes: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.themes, Unset):
            themes = self.themes.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if dark is not UNSET:
            field_dict["dark"] = dark
        if themes is not UNSET:
            field_dict["themes"] = themes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vuetify_themes import VuetifyThemes

        d = src_dict.copy()
        dark = d.pop("dark", UNSET)

        _themes = d.pop("themes", UNSET)
        themes: Union[Unset, VuetifyThemes]
        if isinstance(_themes, Unset):
            themes = UNSET
        else:
            themes = VuetifyThemes.from_dict(_themes)

        vuetify_config = cls(
            dark=dark,
            themes=themes,
        )

        return vuetify_config
