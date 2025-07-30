from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadedFile")


@_attrs_define
class UploadedFile:
    """
    Attributes:
        filename (str):
        id (str):
        content_type (Union[Unset, str]):
    """

    filename: str
    id: str
    content_type: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        filename = self.filename

        id = self.id

        content_type = self.content_type

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "filename": filename,
                "id": id,
            }
        )
        if content_type is not UNSET:
            field_dict["contentType"] = content_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filename = d.pop("filename")

        id = d.pop("id")

        content_type = d.pop("contentType", UNSET)

        uploaded_file = cls(
            filename=filename,
            id=id,
            content_type=content_type,
        )

        return uploaded_file
