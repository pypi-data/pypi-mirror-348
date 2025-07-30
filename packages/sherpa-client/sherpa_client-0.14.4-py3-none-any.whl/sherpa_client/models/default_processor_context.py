from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DefaultProcessorContext")


@attr.s(auto_attribs=True)
class DefaultProcessorContext:
    """
    Attributes:
        language (Union[Unset, str]): language context
        nature (Union[Unset, str]): nature context
    """

    language: Union[Unset, str] = UNSET
    nature: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        language = self.language
        nature = self.nature

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if language is not UNSET:
            field_dict["language"] = language
        if nature is not UNSET:
            field_dict["nature"] = nature

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        language = d.pop("language", UNSET)

        nature = d.pop("nature", UNSET)

        default_processor_context = cls(
            language=language,
            nature=nature,
        )

        return default_processor_context
