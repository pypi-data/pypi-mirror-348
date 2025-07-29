from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ThemeMedia")


@_attrs_define
class ThemeMedia:
    """Images and videos on signin page

    Attributes:
        app_bar_image (Union[Unset, str]):
        bg_image (Union[Unset, str]):
        bg_video (Union[Unset, str]):
    """

    app_bar_image: Union[Unset, str] = UNSET
    bg_image: Union[Unset, str] = UNSET
    bg_video: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        app_bar_image = self.app_bar_image

        bg_image = self.bg_image

        bg_video = self.bg_video

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if app_bar_image is not UNSET:
            field_dict["appBarImage"] = app_bar_image
        if bg_image is not UNSET:
            field_dict["bgImage"] = bg_image
        if bg_video is not UNSET:
            field_dict["bgVideo"] = bg_video

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        app_bar_image = d.pop("appBarImage", UNSET)

        bg_image = d.pop("bgImage", UNSET)

        bg_video = d.pop("bgVideo", UNSET)

        theme_media = cls(
            app_bar_image=app_bar_image,
            bg_image=bg_image,
            bg_video=bg_video,
        )

        return theme_media
