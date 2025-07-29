from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.app_config import AppConfig
    from ..models.vuetify_config import VuetifyConfig


T = TypeVar("T", bound="ThemeConfig")


@_attrs_define
class ThemeConfig:
    """
    Attributes:
        app (Union[Unset, AppConfig]):
        vuetify (Union[Unset, VuetifyConfig]): Standard configuration
    """

    app: Union[Unset, "AppConfig"] = UNSET
    vuetify: Union[Unset, "VuetifyConfig"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        app: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.app, Unset):
            app = self.app.to_dict()

        vuetify: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.vuetify, Unset):
            vuetify = self.vuetify.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if app is not UNSET:
            field_dict["app"] = app
        if vuetify is not UNSET:
            field_dict["vuetify"] = vuetify

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.app_config import AppConfig
        from ..models.vuetify_config import VuetifyConfig

        d = dict(src_dict)
        _app = d.pop("app", UNSET)
        app: Union[Unset, AppConfig]
        if isinstance(_app, Unset):
            app = UNSET
        else:
            app = AppConfig.from_dict(_app)

        _vuetify = d.pop("vuetify", UNSET)
        vuetify: Union[Unset, VuetifyConfig]
        if isinstance(_vuetify, Unset):
            vuetify = UNSET
        else:
            vuetify = VuetifyConfig.from_dict(_vuetify)

        theme_config = cls(
            app=app,
            vuetify=vuetify,
        )

        return theme_config
