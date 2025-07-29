from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="AnnotatedDocAltText")


@_attrs_define
class AnnotatedDocAltText:
    """A document alternative text

    Attributes:
        name (str): The alternative text name
        text (str): The alternative text
    """

    name: str
    text: str

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        text = self.text

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        text = d.pop("text")

        annotated_doc_alt_text = cls(
            name=name,
            text=text,
        )

        return annotated_doc_alt_text
