from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="SimpleGroup")


@attr.s(auto_attribs=True)
class SimpleGroup:
    """
    Attributes:
        label (str):
        name (str):
    """

    label: str
    name: str

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        name = d.pop("name")

        simple_group = cls(
            label=label,
            name=name,
        )

        return simple_group
