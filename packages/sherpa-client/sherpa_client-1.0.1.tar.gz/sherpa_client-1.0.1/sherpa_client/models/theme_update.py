from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.theme_config import ThemeConfig


T = TypeVar("T", bound="ThemeUpdate")


@_attrs_define
class ThemeUpdate:
    """
    Attributes:
        config (Union[Unset, ThemeConfig]):
        deleted_media_files (Union[Unset, list[str]]):
        label (Union[Unset, str]):
    """

    config: Union[Unset, "ThemeConfig"] = UNSET
    deleted_media_files: Union[Unset, list[str]] = UNSET
    label: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.config, Unset):
            config = self.config.to_dict()

        deleted_media_files: Union[Unset, list[str]] = UNSET
        if not isinstance(self.deleted_media_files, Unset):
            deleted_media_files = self.deleted_media_files

        label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if config is not UNSET:
            field_dict["config"] = config
        if deleted_media_files is not UNSET:
            field_dict["deletedMediaFiles"] = deleted_media_files
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.theme_config import ThemeConfig

        d = dict(src_dict)
        _config = d.pop("config", UNSET)
        config: Union[Unset, ThemeConfig]
        if isinstance(_config, Unset):
            config = UNSET
        else:
            config = ThemeConfig.from_dict(_config)

        deleted_media_files = cast(list[str], d.pop("deletedMediaFiles", UNSET))

        label = d.pop("label", UNSET)

        theme_update = cls(
            config=config,
            deleted_media_files=deleted_media_files,
            label=label,
        )

        return theme_update
