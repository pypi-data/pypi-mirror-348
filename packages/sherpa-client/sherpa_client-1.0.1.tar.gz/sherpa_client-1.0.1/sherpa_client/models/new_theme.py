from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.theme_config import ThemeConfig


T = TypeVar("T", bound="NewTheme")


@_attrs_define
class NewTheme:
    """
    Attributes:
        config (ThemeConfig):
        label (str):
    """

    config: "ThemeConfig"
    label: str

    def to_dict(self) -> dict[str, Any]:
        config = self.config.to_dict()

        label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "config": config,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.theme_config import ThemeConfig

        d = dict(src_dict)
        config = ThemeConfig.from_dict(d.pop("config"))

        label = d.pop("label")

        new_theme = cls(
            config=config,
            label=label,
        )

        return new_theme
