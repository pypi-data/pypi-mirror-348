from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_migration_operation import BatchMigrationOperation


T = TypeVar("T", bound="BatchChownChmodMigration")


@_attrs_define
class BatchChownChmodMigration:
    """
    Attributes:
        operations (list['BatchMigrationOperation']):
        share_project_with_previous_owner (Union[Unset, bool]):  Default: True.
    """

    operations: list["BatchMigrationOperation"]
    share_project_with_previous_owner: Union[Unset, bool] = True

    def to_dict(self) -> dict[str, Any]:
        operations = []
        for operations_item_data in self.operations:
            operations_item = operations_item_data.to_dict()
            operations.append(operations_item)

        share_project_with_previous_owner = self.share_project_with_previous_owner

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "operations": operations,
            }
        )
        if share_project_with_previous_owner is not UNSET:
            field_dict["shareProjectWithPreviousOwner"] = (
                share_project_with_previous_owner
            )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_migration_operation import BatchMigrationOperation

        d = dict(src_dict)
        operations = []
        _operations = d.pop("operations")
        for operations_item_data in _operations:
            operations_item = BatchMigrationOperation.from_dict(operations_item_data)

            operations.append(operations_item)

        share_project_with_previous_owner = d.pop(
            "shareProjectWithPreviousOwner", UNSET
        )

        batch_chown_chmod_migration = cls(
            operations=operations,
            share_project_with_previous_owner=share_project_with_previous_owner,
        )

        return batch_chown_chmod_migration
