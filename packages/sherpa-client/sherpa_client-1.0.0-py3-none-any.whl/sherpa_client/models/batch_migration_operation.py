from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.batch_migration_operation_users import BatchMigrationOperationUsers
    from ..models.batch_migration_receive import BatchMigrationReceive


T = TypeVar("T", bound="BatchMigrationOperation")


@_attrs_define
class BatchMigrationOperation:
    """
    Attributes:
        receive (BatchMigrationReceive):
        users (BatchMigrationOperationUsers): MongoDB filter matching users
    """

    receive: "BatchMigrationReceive"
    users: "BatchMigrationOperationUsers"

    def to_dict(self) -> dict[str, Any]:
        receive = self.receive.to_dict()

        users = self.users.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "receive": receive,
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_migration_operation_users import (
            BatchMigrationOperationUsers,
        )
        from ..models.batch_migration_receive import BatchMigrationReceive

        d = dict(src_dict)
        receive = BatchMigrationReceive.from_dict(d.pop("receive"))

        users = BatchMigrationOperationUsers.from_dict(d.pop("users"))

        batch_migration_operation = cls(
            receive=receive,
            users=users,
        )

        return batch_migration_operation
