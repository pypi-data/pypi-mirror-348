from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BatchMigrationReceive")


@attr.s(auto_attribs=True)
class BatchMigrationReceive:
    """
    Attributes:
        ownership (Union[Unset, List[str]]):
        read_access (Union[Unset, List[str]]):
        write_access (Union[Unset, List[str]]):
    """

    ownership: Union[Unset, List[str]] = UNSET
    read_access: Union[Unset, List[str]] = UNSET
    write_access: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        ownership: Union[Unset, List[str]] = UNSET
        if not isinstance(self.ownership, Unset):
            ownership = self.ownership

        read_access: Union[Unset, List[str]] = UNSET
        if not isinstance(self.read_access, Unset):
            read_access = self.read_access

        write_access: Union[Unset, List[str]] = UNSET
        if not isinstance(self.write_access, Unset):
            write_access = self.write_access

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if ownership is not UNSET:
            field_dict["ownership"] = ownership
        if read_access is not UNSET:
            field_dict["readAccess"] = read_access
        if write_access is not UNSET:
            field_dict["writeAccess"] = write_access

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ownership = cast(List[str], d.pop("ownership", UNSET))

        read_access = cast(List[str], d.pop("readAccess", UNSET))

        write_access = cast(List[str], d.pop("writeAccess", UNSET))

        batch_migration_receive = cls(
            ownership=ownership,
            read_access=read_access,
            write_access=write_access,
        )

        return batch_migration_receive
