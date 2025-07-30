from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.vuetify_themes import VuetifyThemes


T = TypeVar("T", bound="VuetifyConfig")


@_attrs_define
class VuetifyConfig:
    """Standard configuration

    Attributes:
        dark (Union[Unset, bool]):  Default: False.
        themes (Union[Unset, VuetifyThemes]): Standard themes
    """

    dark: Union[Unset, bool] = False
    themes: Union[Unset, "VuetifyThemes"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        dark = self.dark

        themes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.themes, Unset):
            themes = self.themes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if dark is not UNSET:
            field_dict["dark"] = dark
        if themes is not UNSET:
            field_dict["themes"] = themes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.vuetify_themes import VuetifyThemes

        d = dict(src_dict)
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
