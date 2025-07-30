from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

import attr

if TYPE_CHECKING:
    from ..models.batch_migration_operation_users import BatchMigrationOperationUsers
    from ..models.batch_migration_receive import BatchMigrationReceive


T = TypeVar("T", bound="BatchMigrationOperation")


@attr.s(auto_attribs=True)
class BatchMigrationOperation:
    """
    Attributes:
        receive (BatchMigrationReceive):
        users (BatchMigrationOperationUsers): MongoDB filter matching users
    """

    receive: "BatchMigrationReceive"
    users: "BatchMigrationOperationUsers"

    def to_dict(self) -> Dict[str, Any]:
        receive = self.receive.to_dict()

        users = self.users.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "receive": receive,
                "users": users,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch_migration_operation_users import BatchMigrationOperationUsers
        from ..models.batch_migration_receive import BatchMigrationReceive

        d = src_dict.copy()
        receive = BatchMigrationReceive.from_dict(d.pop("receive"))

        users = BatchMigrationOperationUsers.from_dict(d.pop("users"))

        batch_migration_operation = cls(
            receive=receive,
            users=users,
        )

        return batch_migration_operation
