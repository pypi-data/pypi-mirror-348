from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RoleDesc")


@_attrs_define
class RoleDesc:
    """
    Attributes:
        label (str):
        permissions (list[str]):
        rolename (str):
        type_ (str):
        created_at (Union[Unset, str]):
        created_by (Union[Unset, str]):
        group_name (Union[Unset, str]):
        modified_at (Union[Unset, str]):
        modified_by (Union[Unset, str]):
        predefined (Union[Unset, bool]):
    """

    label: str
    permissions: list[str]
    rolename: str
    type_: str
    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    group_name: Union[Unset, str] = UNSET
    modified_at: Union[Unset, str] = UNSET
    modified_by: Union[Unset, str] = UNSET
    predefined: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        permissions = self.permissions

        rolename = self.rolename

        type_ = self.type_

        created_at = self.created_at

        created_by = self.created_by

        group_name = self.group_name

        modified_at = self.modified_at

        modified_by = self.modified_by

        predefined = self.predefined

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "permissions": permissions,
                "rolename": rolename,
                "type": type_,
            }
        )
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if group_name is not UNSET:
            field_dict["groupName"] = group_name
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if modified_by is not UNSET:
            field_dict["modifiedBy"] = modified_by
        if predefined is not UNSET:
            field_dict["predefined"] = predefined

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        permissions = cast(list[str], d.pop("permissions"))

        rolename = d.pop("rolename")

        type_ = d.pop("type")

        created_at = d.pop("createdAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        group_name = d.pop("groupName", UNSET)

        modified_at = d.pop("modifiedAt", UNSET)

        modified_by = d.pop("modifiedBy", UNSET)

        predefined = d.pop("predefined", UNSET)

        role_desc = cls(
            label=label,
            permissions=permissions,
            rolename=rolename,
            type_=type_,
            created_at=created_at,
            created_by=created_by,
            group_name=group_name,
            modified_at=modified_at,
            modified_by=modified_by,
            predefined=predefined,
        )

        return role_desc
