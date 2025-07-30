import json
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, Tuple, Type, TypeVar, Union

import attr

from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.theme_update import ThemeUpdate


T = TypeVar("T", bound="UpdateThemeForm")


@attr.s(auto_attribs=True)
class UpdateThemeForm:
    """
    Attributes:
        app_bar_image (Union[Unset, File]):  logo image
        bg_image (Union[Unset, File]):  background image
        bg_video (Union[Unset, File]):  background video
        theme (Union[Unset, ThemeUpdate]):
    """

    app_bar_image: Union[Unset, File] = UNSET
    bg_image: Union[Unset, File] = UNSET
    bg_video: Union[Unset, File] = UNSET
    theme: Union[Unset, "ThemeUpdate"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        app_bar_image: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.app_bar_image, Unset):
            app_bar_image = self.app_bar_image.to_tuple()

        bg_image: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.bg_image, Unset):
            bg_image = self.bg_image.to_tuple()

        bg_video: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.bg_video, Unset):
            bg_video = self.bg_video.to_tuple()

        theme: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.theme, Unset):
            theme = self.theme.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if app_bar_image is not UNSET:
            field_dict["appBarImage"] = app_bar_image
        if bg_image is not UNSET:
            field_dict["bgImage"] = bg_image
        if bg_video is not UNSET:
            field_dict["bgVideo"] = bg_video
        if theme is not UNSET:
            field_dict["theme"] = theme

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        app_bar_image: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.app_bar_image, Unset):
            app_bar_image = self.app_bar_image.to_tuple()

        bg_image: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.bg_image, Unset):
            bg_image = self.bg_image.to_tuple()

        bg_video: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.bg_video, Unset):
            bg_video = self.bg_video.to_tuple()

        theme: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.theme, Unset):
            theme = (None, json.dumps(self.theme.to_dict()).encode(), "application/json")

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if app_bar_image is not UNSET:
            field_dict["appBarImage"] = app_bar_image
        if bg_image is not UNSET:
            field_dict["bgImage"] = bg_image
        if bg_video is not UNSET:
            field_dict["bgVideo"] = bg_video
        if theme is not UNSET:
            field_dict["theme"] = theme

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.theme_update import ThemeUpdate

        d = src_dict.copy()
        _app_bar_image = d.pop("appBarImage", UNSET)
        app_bar_image: Union[Unset, File]
        if isinstance(_app_bar_image, Unset):
            app_bar_image = UNSET
        else:
            app_bar_image = File(payload=BytesIO(_app_bar_image))

        _bg_image = d.pop("bgImage", UNSET)
        bg_image: Union[Unset, File]
        if isinstance(_bg_image, Unset):
            bg_image = UNSET
        else:
            bg_image = File(payload=BytesIO(_bg_image))

        _bg_video = d.pop("bgVideo", UNSET)
        bg_video: Union[Unset, File]
        if isinstance(_bg_video, Unset):
            bg_video = UNSET
        else:
            bg_video = File(payload=BytesIO(_bg_video))

        _theme = d.pop("theme", UNSET)
        theme: Union[Unset, ThemeUpdate]
        if isinstance(_theme, Unset):
            theme = UNSET
        else:
            theme = ThemeUpdate.from_dict(_theme)

        update_theme_form = cls(
            app_bar_image=app_bar_image,
            bg_image=bg_image,
            bg_video=bg_video,
            theme=theme,
        )

        return update_theme_form
