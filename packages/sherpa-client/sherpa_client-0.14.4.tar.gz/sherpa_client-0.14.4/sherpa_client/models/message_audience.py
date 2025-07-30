from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="MessageAudience")


@attr.s(auto_attribs=True)
class MessageAudience:
    """
    Attributes:
        group_names (Union[Unset, List[str]]):
        usernames (Union[Unset, List[str]]):
    """

    group_names: Union[Unset, List[str]] = UNSET
    usernames: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        group_names: Union[Unset, List[str]] = UNSET
        if not isinstance(self.group_names, Unset):
            group_names = self.group_names

        usernames: Union[Unset, List[str]] = UNSET
        if not isinstance(self.usernames, Unset):
            usernames = self.usernames

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if group_names is not UNSET:
            field_dict["groupNames"] = group_names
        if usernames is not UNSET:
            field_dict["usernames"] = usernames

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        group_names = cast(List[str], d.pop("groupNames", UNSET))

        usernames = cast(List[str], d.pop("usernames", UNSET))

        message_audience = cls(
            group_names=group_names,
            usernames=usernames,
        )

        return message_audience
