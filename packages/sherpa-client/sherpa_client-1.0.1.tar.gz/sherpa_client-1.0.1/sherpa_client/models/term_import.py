from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.term_importer_spec import TermImporterSpec
    from ..models.uploaded_file import UploadedFile


T = TypeVar("T", bound="TermImport")


@_attrs_define
class TermImport:
    """
    Attributes:
        files (list['UploadedFile']):
        importer (TermImporterSpec):
    """

    files: list["UploadedFile"]
    importer: "TermImporterSpec"

    def to_dict(self) -> dict[str, Any]:
        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        importer = self.importer.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "files": files,
                "importer": importer,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.term_importer_spec import TermImporterSpec
        from ..models.uploaded_file import UploadedFile

        d = dict(src_dict)
        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = UploadedFile.from_dict(files_item_data)

            files.append(files_item)

        importer = TermImporterSpec.from_dict(d.pop("importer"))

        term_import = cls(
            files=files,
            importer=importer,
        )

        return term_import
