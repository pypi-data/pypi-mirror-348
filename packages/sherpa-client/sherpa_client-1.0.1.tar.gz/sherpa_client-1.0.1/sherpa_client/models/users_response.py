from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_response import UserResponse


T = TypeVar("T", bound="UsersResponse")


@_attrs_define
class UsersResponse:
    """
    Attributes:
        users (Union[Unset, list['UserResponse']]):
    """

    users: Union[Unset, list["UserResponse"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        users: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_response import UserResponse

        d = dict(src_dict)
        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = UserResponse.from_dict(users_item_data)

            users.append(users_item)

        users_response = cls(
            users=users,
        )

        return users_response
