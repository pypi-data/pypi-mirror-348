from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="BatchMigrationReceive")


@_attrs_define
class BatchMigrationReceive:
    """
    Attributes:
        ownership (Union[Unset, list[str]]):
        read_access (Union[Unset, list[str]]):
        write_access (Union[Unset, list[str]]):
    """

    ownership: Union[Unset, list[str]] = UNSET
    read_access: Union[Unset, list[str]] = UNSET
    write_access: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        ownership: Union[Unset, list[str]] = UNSET
        if not isinstance(self.ownership, Unset):
            ownership = self.ownership

        read_access: Union[Unset, list[str]] = UNSET
        if not isinstance(self.read_access, Unset):
            read_access = self.read_access

        write_access: Union[Unset, list[str]] = UNSET
        if not isinstance(self.write_access, Unset):
            write_access = self.write_access

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if ownership is not UNSET:
            field_dict["ownership"] = ownership
        if read_access is not UNSET:
            field_dict["readAccess"] = read_access
        if write_access is not UNSET:
            field_dict["writeAccess"] = write_access

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ownership = cast(list[str], d.pop("ownership", UNSET))

        read_access = cast(list[str], d.pop("readAccess", UNSET))

        write_access = cast(list[str], d.pop("writeAccess", UNSET))

        batch_migration_receive = cls(
            ownership=ownership,
            read_access=read_access,
            write_access=write_access,
        )

        return batch_migration_receive
