from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_chown_chmod_migration import BatchChownChmodMigration
    from ..models.batch_chown_chmod_virtual_target_users_item import BatchChownChmodVirtualTargetUsersItem


T = TypeVar("T", bound="BatchChownChmod")


@attr.s(auto_attribs=True)
class BatchChownChmod:
    """
    Attributes:
        migration (BatchChownChmodMigration):
        virtual_target_users (Union[Unset, List['BatchChownChmodVirtualTargetUsersItem']]):
        virtual_target_users_from_migration (Union[Unset, bool]):
        warn_non_chowned_projects (Union[Unset, bool]):
    """

    migration: "BatchChownChmodMigration"
    virtual_target_users: Union[Unset, List["BatchChownChmodVirtualTargetUsersItem"]] = UNSET
    virtual_target_users_from_migration: Union[Unset, bool] = False
    warn_non_chowned_projects: Union[Unset, bool] = False

    def to_dict(self) -> Dict[str, Any]:
        migration = self.migration.to_dict()

        virtual_target_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.virtual_target_users, Unset):
            virtual_target_users = []
            for virtual_target_users_item_data in self.virtual_target_users:
                virtual_target_users_item = virtual_target_users_item_data.to_dict()

                virtual_target_users.append(virtual_target_users_item)

        virtual_target_users_from_migration = self.virtual_target_users_from_migration
        warn_non_chowned_projects = self.warn_non_chowned_projects

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "migration": migration,
            }
        )
        if virtual_target_users is not UNSET:
            field_dict["virtualTargetUsers"] = virtual_target_users
        if virtual_target_users_from_migration is not UNSET:
            field_dict["virtualTargetUsersFromMigration"] = virtual_target_users_from_migration
        if warn_non_chowned_projects is not UNSET:
            field_dict["warnNonChownedProjects"] = warn_non_chowned_projects

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch_chown_chmod_migration import BatchChownChmodMigration
        from ..models.batch_chown_chmod_virtual_target_users_item import BatchChownChmodVirtualTargetUsersItem

        d = src_dict.copy()
        migration = BatchChownChmodMigration.from_dict(d.pop("migration"))

        virtual_target_users = []
        _virtual_target_users = d.pop("virtualTargetUsers", UNSET)
        for virtual_target_users_item_data in _virtual_target_users or []:
            virtual_target_users_item = BatchChownChmodVirtualTargetUsersItem.from_dict(virtual_target_users_item_data)

            virtual_target_users.append(virtual_target_users_item)

        virtual_target_users_from_migration = d.pop("virtualTargetUsersFromMigration", UNSET)

        warn_non_chowned_projects = d.pop("warnNonChownedProjects", UNSET)

        batch_chown_chmod = cls(
            migration=migration,
            virtual_target_users=virtual_target_users,
            virtual_target_users_from_migration=virtual_target_users_from_migration,
            warn_non_chowned_projects=warn_non_chowned_projects,
        )

        return batch_chown_chmod
