import json
from collections.abc import Mapping
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.convert_format_annotation_plan import ConvertFormatAnnotationPlan


T = TypeVar("T", bound="FormatBinaryForm")


@_attrs_define
class FormatBinaryForm:
    """
    Attributes:
        file (Union[Unset, File]):  binary file to be converted and annotated
        plan (Union[Unset, ConvertFormatAnnotationPlan]):
    """

    file: Union[Unset, File] = UNSET
    plan: Union[Unset, "ConvertFormatAnnotationPlan"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

        plan: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if file is not UNSET:
            field_dict["file"] = file
        if plan is not UNSET:
            field_dict["plan"] = plan

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

        plan: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.plan, Unset):
            plan = (None, json.dumps(self.plan.to_dict()).encode(), "application/json")

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if file is not UNSET:
            field_dict["file"] = file
        if plan is not UNSET:
            field_dict["plan"] = plan

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.convert_format_annotation_plan import ConvertFormatAnnotationPlan

        d = dict(src_dict)
        _file = d.pop("file", UNSET)
        file: Union[Unset, File]
        if isinstance(_file, Unset):
            file = UNSET
        else:
            file = File(payload=BytesIO(_file))

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, ConvertFormatAnnotationPlan]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = ConvertFormatAnnotationPlan.from_dict(_plan)

        format_binary_form = cls(
            file=file,
            plan=plan,
        )

        return format_binary_form
