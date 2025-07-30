from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ThemeId")


@attr.s(auto_attribs=True)
class ThemeId:
    """
    Attributes:
        id (str):
    """

    id: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        theme_id = cls(
            id=id,
        )

        return theme_id
