from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.theme_config import ThemeConfig


T = TypeVar("T", bound="Theme")


@attr.s(auto_attribs=True)
class Theme:
    """
    Attributes:
        config (ThemeConfig):
        id (str):
        label (str):
        created_at (Union[Unset, str]):
        created_by (Union[Unset, str]):
        modified_at (Union[Unset, str]):
        modified_by (Union[Unset, str]):
    """

    config: "ThemeConfig"
    id: str
    label: str
    created_at: Union[Unset, str] = UNSET
    created_by: Union[Unset, str] = UNSET
    modified_at: Union[Unset, str] = UNSET
    modified_by: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        config = self.config.to_dict()

        id = self.id
        label = self.label
        created_at = self.created_at
        created_by = self.created_by
        modified_at = self.modified_at
        modified_by = self.modified_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "config": config,
                "id": id,
                "label": label,
            }
        )
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if modified_by is not UNSET:
            field_dict["modifiedBy"] = modified_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.theme_config import ThemeConfig

        d = src_dict.copy()
        config = ThemeConfig.from_dict(d.pop("config"))

        id = d.pop("id")

        label = d.pop("label")

        created_at = d.pop("createdAt", UNSET)

        created_by = d.pop("createdBy", UNSET)

        modified_at = d.pop("modifiedAt", UNSET)

        modified_by = d.pop("modifiedBy", UNSET)

        theme = cls(
            config=config,
            id=id,
            label=label,
            created_at=created_at,
            created_by=created_by,
            modified_at=modified_at,
            modified_by=modified_by,
        )

        return theme
