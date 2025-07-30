from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.gazetteer_patch_parameters import GazetteerPatchParameters


T = TypeVar("T", bound="GazetteerPatch")


@_attrs_define
class GazetteerPatch:
    """
    Attributes:
        email_notification (Union[Unset, bool]):
        favorite (Union[Unset, bool]):
        label (Union[Unset, str]):
        parameters (Union[Unset, GazetteerPatchParameters]):
        tags (Union[Unset, list[str]]):
    """

    email_notification: Union[Unset, bool] = UNSET
    favorite: Union[Unset, bool] = UNSET
    label: Union[Unset, str] = UNSET
    parameters: Union[Unset, "GazetteerPatchParameters"] = UNSET
    tags: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        email_notification = self.email_notification

        favorite = self.favorite

        label = self.label

        parameters: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if email_notification is not UNSET:
            field_dict["emailNotification"] = email_notification
        if favorite is not UNSET:
            field_dict["favorite"] = favorite
        if label is not UNSET:
            field_dict["label"] = label
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.gazetteer_patch_parameters import GazetteerPatchParameters

        d = dict(src_dict)
        email_notification = d.pop("emailNotification", UNSET)

        favorite = d.pop("favorite", UNSET)

        label = d.pop("label", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, GazetteerPatchParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = GazetteerPatchParameters.from_dict(_parameters)

        tags = cast(list[str], d.pop("tags", UNSET))

        gazetteer_patch = cls(
            email_notification=email_notification,
            favorite=favorite,
            label=label,
            parameters=parameters,
            tags=tags,
        )

        return gazetteer_patch
