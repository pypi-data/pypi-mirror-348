from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.theme_config import ThemeConfig


T = TypeVar("T", bound="NewTheme")


@attr.s(auto_attribs=True)
class NewTheme:
    """
    Attributes:
        config (ThemeConfig):
        label (str):
    """

    config: "ThemeConfig"
    label: str

    def to_dict(self) -> Dict[str, Any]:
        config = self.config.to_dict()

        label = self.label

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "config": config,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.theme_config import ThemeConfig

        d = src_dict.copy()
        config = ThemeConfig.from_dict(d.pop("config"))

        label = d.pop("label")

        new_theme = cls(
            config=config,
            label=label,
        )

        return new_theme
