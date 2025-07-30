from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="AnnotatedDocAltText")


@attr.s(auto_attribs=True)
class AnnotatedDocAltText:
    """A document alternative text

    Attributes:
        name (str): The alternative text name
        text (str): The alternative text
    """

    name: str
    text: str

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        text = d.pop("text")

        annotated_doc_alt_text = cls(
            name=name,
            text=text,
        )

        return annotated_doc_alt_text
