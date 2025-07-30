from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.new_group_desc_mapping_discriminator import NewGroupDescMappingDiscriminator
from ..types import UNSET, Unset

T = TypeVar("T", bound="NewGroupDesc")


@attr.s(auto_attribs=True)
class NewGroupDesc:
    """
    Attributes:
        label (str):
        attached_roles (Union[Unset, List[str]]):
        identifier (Union[Unset, str]):
        login_allowed (Union[Unset, bool]):
        mapping_discriminator (Union[Unset, NewGroupDescMappingDiscriminator]):
        max_docs_per_project (Union[Unset, int]):
        max_projects (Union[Unset, int]):
        max_projects_per_user (Union[Unset, int]):
        max_users (Union[Unset, int]):
        system_attached_roles (Union[Unset, List[str]]):
    """

    label: str
    attached_roles: Union[Unset, List[str]] = UNSET
    identifier: Union[Unset, str] = UNSET
    login_allowed: Union[Unset, bool] = UNSET
    mapping_discriminator: Union[Unset, NewGroupDescMappingDiscriminator] = UNSET
    max_docs_per_project: Union[Unset, int] = UNSET
    max_projects: Union[Unset, int] = UNSET
    max_projects_per_user: Union[Unset, int] = UNSET
    max_users: Union[Unset, int] = UNSET
    system_attached_roles: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        attached_roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.attached_roles, Unset):
            attached_roles = self.attached_roles

        identifier = self.identifier
        login_allowed = self.login_allowed
        mapping_discriminator: Union[Unset, str] = UNSET
        if not isinstance(self.mapping_discriminator, Unset):
            mapping_discriminator = self.mapping_discriminator.value

        max_docs_per_project = self.max_docs_per_project
        max_projects = self.max_projects
        max_projects_per_user = self.max_projects_per_user
        max_users = self.max_users
        system_attached_roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.system_attached_roles, Unset):
            system_attached_roles = self.system_attached_roles

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
            }
        )
        if attached_roles is not UNSET:
            field_dict["attachedRoles"] = attached_roles
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if login_allowed is not UNSET:
            field_dict["loginAllowed"] = login_allowed
        if mapping_discriminator is not UNSET:
            field_dict["mappingDiscriminator"] = mapping_discriminator
        if max_docs_per_project is not UNSET:
            field_dict["maxDocsPerProject"] = max_docs_per_project
        if max_projects is not UNSET:
            field_dict["maxProjects"] = max_projects
        if max_projects_per_user is not UNSET:
            field_dict["maxProjectsPerUser"] = max_projects_per_user
        if max_users is not UNSET:
            field_dict["maxUsers"] = max_users
        if system_attached_roles is not UNSET:
            field_dict["systemAttachedRoles"] = system_attached_roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        attached_roles = cast(List[str], d.pop("attachedRoles", UNSET))

        identifier = d.pop("identifier", UNSET)

        login_allowed = d.pop("loginAllowed", UNSET)

        _mapping_discriminator = d.pop("mappingDiscriminator", UNSET)
        mapping_discriminator: Union[Unset, NewGroupDescMappingDiscriminator]
        if isinstance(_mapping_discriminator, Unset):
            mapping_discriminator = UNSET
        else:
            mapping_discriminator = NewGroupDescMappingDiscriminator(_mapping_discriminator)

        max_docs_per_project = d.pop("maxDocsPerProject", UNSET)

        max_projects = d.pop("maxProjects", UNSET)

        max_projects_per_user = d.pop("maxProjectsPerUser", UNSET)

        max_users = d.pop("maxUsers", UNSET)

        system_attached_roles = cast(List[str], d.pop("systemAttachedRoles", UNSET))

        new_group_desc = cls(
            label=label,
            attached_roles=attached_roles,
            identifier=identifier,
            login_allowed=login_allowed,
            mapping_discriminator=mapping_discriminator,
            max_docs_per_project=max_docs_per_project,
            max_projects=max_projects,
            max_projects_per_user=max_projects_per_user,
            max_users=max_users,
            system_attached_roles=system_attached_roles,
        )

        return new_group_desc
