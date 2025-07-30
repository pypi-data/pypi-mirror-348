from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_migration_operation import BatchMigrationOperation


T = TypeVar("T", bound="BatchChownChmodMigration")


@attr.s(auto_attribs=True)
class BatchChownChmodMigration:
    """
    Attributes:
        operations (List['BatchMigrationOperation']):
        share_project_with_previous_owner (Union[Unset, bool]):  Default: True.
    """

    operations: List["BatchMigrationOperation"]
    share_project_with_previous_owner: Union[Unset, bool] = True

    def to_dict(self) -> Dict[str, Any]:
        operations = []
        for operations_item_data in self.operations:
            operations_item = operations_item_data.to_dict()

            operations.append(operations_item)

        share_project_with_previous_owner = self.share_project_with_previous_owner

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "operations": operations,
            }
        )
        if share_project_with_previous_owner is not UNSET:
            field_dict["shareProjectWithPreviousOwner"] = share_project_with_previous_owner

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch_migration_operation import BatchMigrationOperation

        d = src_dict.copy()
        operations = []
        _operations = d.pop("operations")
        for operations_item_data in _operations:
            operations_item = BatchMigrationOperation.from_dict(operations_item_data)

            operations.append(operations_item)

        share_project_with_previous_owner = d.pop("shareProjectWithPreviousOwner", UNSET)

        batch_chown_chmod_migration = cls(
            operations=operations,
            share_project_with_previous_owner=share_project_with_previous_owner,
        )

        return batch_chown_chmod_migration
