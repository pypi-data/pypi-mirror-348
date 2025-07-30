from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.simple_group_membership_desc import SimpleGroupMembershipDesc


T = TypeVar("T", bound="UserResponse")


@attr.s(auto_attribs=True)
class UserResponse:
    """
    Attributes:
        profilename (str):
        username (str):
        created_at (Union[Unset, str]):
        created_by (Union[Unset, str]):
        disabled (Union[Unset, bool]):
        email (Union[Unset, str]):
        groups (Union[Unset, List['SimpleGroupMembershipDesc']]):
        permissions (Union[Unset, List[str]]):
        roles (Union[Unset, List[str]]):
    """

    profilename: str
    username: str
    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    disabled: Union[Unset, bool] = UNSET
    email: Union[Unset, str] = UNSET
    groups: Union[Unset, List["SimpleGroupMembershipDesc"]] = UNSET
    permissions: Union[Unset, List[str]] = UNSET
    roles: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        profilename = self.profilename
        username = self.username
        created_at = self.created_at
        created_by = self.created_by
        disabled = self.disabled
        email = self.email
        groups: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for groups_item_data in self.groups:
                groups_item = groups_item_data.to_dict()

                groups.append(groups_item)

        permissions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions

        roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "profilename": profilename,
                "username": username,
            }
        )
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if email is not UNSET:
            field_dict["email"] = email
        if groups is not UNSET:
            field_dict["groups"] = groups
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if roles is not UNSET:
            field_dict["roles"] = roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.simple_group_membership_desc import SimpleGroupMembershipDesc

        d = src_dict.copy()
        profilename = d.pop("profilename")

        username = d.pop("username")

        created_at = d.pop("createdAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        disabled = d.pop("disabled", UNSET)

        email = d.pop("email", UNSET)

        groups = []
        _groups = d.pop("groups", UNSET)
        for groups_item_data in _groups or []:
            groups_item = SimpleGroupMembershipDesc.from_dict(groups_item_data)

            groups.append(groups_item)

        permissions = cast(List[str], d.pop("permissions", UNSET))

        roles = cast(List[str], d.pop("roles", UNSET))

        user_response = cls(
            profilename=profilename,
            username=username,
            created_at=created_at,
            created_by=created_by,
            disabled=disabled,
            email=email,
            groups=groups,
            permissions=permissions,
            roles=roles,
        )

        return user_response
