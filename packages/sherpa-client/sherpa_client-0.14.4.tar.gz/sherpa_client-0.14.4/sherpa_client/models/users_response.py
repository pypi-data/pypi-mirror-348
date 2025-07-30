from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_response import UserResponse


T = TypeVar("T", bound="UsersResponse")


@attr.s(auto_attribs=True)
class UsersResponse:
    """
    Attributes:
        users (Union[Unset, List['UserResponse']]):
    """

    users: Union[Unset, List["UserResponse"]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()

                users.append(users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.user_response import UserResponse

        d = src_dict.copy()
        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = UserResponse.from_dict(users_item_data)

            users.append(users_item)

        users_response = cls(
            users=users,
        )

        return users_response
