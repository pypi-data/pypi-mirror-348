from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MessageAudience")


@_attrs_define
class MessageAudience:
    """
    Attributes:
        group_names (Union[Unset, list[str]]):
        usernames (Union[Unset, list[str]]):
    """

    group_names: Union[Unset, list[str]] = UNSET
    usernames: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        group_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.group_names, Unset):
            group_names = self.group_names

        usernames: Union[Unset, list[str]] = UNSET
        if not isinstance(self.usernames, Unset):
            usernames = self.usernames

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if group_names is not UNSET:
            field_dict["groupNames"] = group_names
        if usernames is not UNSET:
            field_dict["usernames"] = usernames

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        group_names = cast(list[str], d.pop("groupNames", UNSET))

        usernames = cast(list[str], d.pop("usernames", UNSET))

        message_audience = cls(
            group_names=group_names,
            usernames=usernames,
        )

        return message_audience
