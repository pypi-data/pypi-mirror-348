from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.theme_config import ThemeConfig


T = TypeVar("T", bound="ThemeUpdate")


@attr.s(auto_attribs=True)
class ThemeUpdate:
    """
    Attributes:
        config (Union[Unset, ThemeConfig]):
        deleted_media_files (Union[Unset, List[str]]):
        label (Union[Unset, str]):
    """

    config: Union[Unset, "ThemeConfig"] = UNSET
    deleted_media_files: Union[Unset, List[str]] = UNSET
    label: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        deleted_media_files: Union[Unset, List[str]] = UNSET
        if not isinstance(self.deleted_media_files, Unset):
            deleted_media_files = self.deleted_media_files

        label = self.label

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if deleted_media_files is not UNSET:
            field_dict["deletedMediaFiles"] = deleted_media_files
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.theme_config import ThemeConfig

        d = src_dict.copy()
        _config = d.pop("config", UNSET)
        config: Union[Unset, ThemeConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = ThemeConfig.from_dict(_config)

        deleted_media_files = cast(List[str], d.pop("deletedMediaFiles", UNSET))

        label = d.pop("label", UNSET)

        theme_update = cls(
            config=config,
            deleted_media_files=deleted_media_files,
            label=label,
        )

        return theme_update
