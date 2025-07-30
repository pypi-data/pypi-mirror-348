from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.group_desc_mapping_discriminator import GroupDescMappingDiscriminator
from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupDesc")


@attr.s(auto_attribs=True)
class GroupDesc:
    """
    Attributes:
        label (str):
        login_allowed (bool):
        max_users (int):
        name (str):
        attached_roles (Union[Unset, List[str]]):
        created_at (Union[Unset, str]):
        created_by (Union[Unset, str]):
        identifier (Union[Unset, str]):
        mapping_discriminator (Union[Unset, GroupDescMappingDiscriminator]):
        max_docs_per_project (Union[Unset, int]):
        max_projects (Union[Unset, int]):
        max_projects_per_user (Union[Unset, int]):
        modified_at (Union[Unset, str]):
        modified_by (Union[Unset, str]):
        system_attached_roles (Union[Unset, List[str]]):
    """

    label: str
    login_allowed: bool
    max_users: int
    name: str
    attached_roles: Union[Unset, List[str]] = UNSET
    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    mapping_discriminator: Union[Unset, GroupDescMappingDiscriminator] = UNSET
    max_docs_per_project: Union[Unset, int] = UNSET
    max_projects: Union[Unset, int] = UNSET
    max_projects_per_user: Union[Unset, int] = UNSET
    modified_at: Union[Unset, str] = UNSET
    modified_by: Union[Unset, str] = UNSET
    system_attached_roles: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        login_allowed = self.login_allowed
        max_users = self.max_users
        name = self.name
        attached_roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.attached_roles, Unset):
            attached_roles = self.attached_roles

        created_at = self.created_at
        created_by = self.created_by
        identifier = self.identifier
        mapping_discriminator: Union[Unset, str] = UNSET
        if not isinstance(self.mapping_discriminator, Unset):
            mapping_discriminator = self.mapping_discriminator.value

        max_docs_per_project = self.max_docs_per_project
        max_projects = self.max_projects
        max_projects_per_user = self.max_projects_per_user
        modified_at = self.modified_at
        modified_by = self.modified_by
        system_attached_roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.system_attached_roles, Unset):
            system_attached_roles = self.system_attached_roles

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "loginAllowed": login_allowed,
                "maxUsers": max_users,
                "name": name,
            }
        )
        if attached_roles is not UNSET:
            field_dict["attachedRoles"] = attached_roles
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if mapping_discriminator is not UNSET:
            field_dict["mappingDiscriminator"] = mapping_discriminator
        if max_docs_per_project is not UNSET:
            field_dict["maxDocsPerProject"] = max_docs_per_project
        if max_projects is not UNSET:
            field_dict["maxProjects"] = max_projects
        if max_projects_per_user is not UNSET:
            field_dict["maxProjectsPerUser"] = max_projects_per_user
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if modified_by is not UNSET:
            field_dict["modifiedBy"] = modified_by
        if system_attached_roles is not UNSET:
            field_dict["systemAttachedRoles"] = system_attached_roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        login_allowed = d.pop("loginAllowed")

        max_users = d.pop("maxUsers")

        name = d.pop("name")

        attached_roles = cast(List[str], d.pop("attachedRoles", UNSET))

        created_at = d.pop("createdAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        identifier = d.pop("identifier", UNSET)

        _mapping_discriminator = d.pop("mappingDiscriminator", UNSET)
        mapping_discriminator: Union[Unset, GroupDescMappingDiscriminator]
        if isinstance(_mapping_discriminator, Unset):
            mapping_discriminator = UNSET
        else:
            mapping_discriminator = GroupDescMappingDiscriminator(_mapping_discriminator)

        max_docs_per_project = d.pop("maxDocsPerProject", UNSET)

        max_projects = d.pop("maxProjects", UNSET)

        max_projects_per_user = d.pop("maxProjectsPerUser", UNSET)

        modified_at = d.pop("modifiedAt", UNSET)

        modified_by = d.pop("modifiedBy", UNSET)

        system_attached_roles = cast(List[str], d.pop("systemAttachedRoles", UNSET))

        group_desc = cls(
            label=label,
            login_allowed=login_allowed,
            max_users=max_users,
            name=name,
            attached_roles=attached_roles,
            created_at=created_at,
            created_by=created_by,
            identifier=identifier,
            mapping_discriminator=mapping_discriminator,
            max_docs_per_project=max_docs_per_project,
            max_projects=max_projects,
            max_projects_per_user=max_projects_per_user,
            modified_at=modified_at,
            modified_by=modified_by,
            system_attached_roles=system_attached_roles,
        )

        return group_desc
