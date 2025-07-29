from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DefaultProcessorContext")


@_attrs_define
class DefaultProcessorContext:
    """
    Attributes:
        language (Union[Unset, str]): language context
        nature (Union[Unset, str]): nature context
    """

    language: Union[Unset, str] = UNSET
    nature: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        language = self.language

        nature = self.nature

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if language is not UNSET:
            field_dict["language"] = language
        if nature is not UNSET:
            field_dict["nature"] = nature

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        language = d.pop("language", UNSET)

        nature = d.pop("nature", UNSET)

        default_processor_context = cls(
            language=language,
            nature=nature,
        )

        return default_processor_context
