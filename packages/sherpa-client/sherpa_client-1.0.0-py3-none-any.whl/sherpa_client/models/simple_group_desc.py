from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.simple_group_desc_mapping_discriminator import (
    SimpleGroupDescMappingDiscriminator,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleGroupDesc")


@_attrs_define
class SimpleGroupDesc:
    """
    Attributes:
        label (str):
        name (str):
        identifier (Union[Unset, str]):
        mapping_discriminator (Union[Unset, SimpleGroupDescMappingDiscriminator]):
    """

    label: str
    name: str
    identifier: Union[Unset, str] = UNSET
    mapping_discriminator: Union[Unset, SimpleGroupDescMappingDiscriminator] = UNSET

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        name = self.name

        identifier = self.identifier

        mapping_discriminator: Union[Unset, str] = UNSET
        if not isinstance(self.mapping_discriminator, Unset):
            mapping_discriminator = self.mapping_discriminator.value

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "label": label,
                "name": name,
            }
        )
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if mapping_discriminator is not UNSET:
            field_dict["mappingDiscriminator"] = mapping_discriminator

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        name = d.pop("name")

        identifier = d.pop("identifier", UNSET)

        _mapping_discriminator = d.pop("mappingDiscriminator", UNSET)
        mapping_discriminator: Union[Unset, SimpleGroupDescMappingDiscriminator]
        if isinstance(_mapping_discriminator, Unset):
            mapping_discriminator = UNSET
        else:
            mapping_discriminator = SimpleGroupDescMappingDiscriminator(
                _mapping_discriminator
            )

        simple_group_desc = cls(
            label=label,
            name=name,
            identifier=identifier,
            mapping_discriminator=mapping_discriminator,
        )

        return simple_group_desc
