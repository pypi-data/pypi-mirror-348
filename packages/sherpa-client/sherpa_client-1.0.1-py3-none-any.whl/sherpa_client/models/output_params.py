from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="OutputParams")


@_attrs_define
class OutputParams:
    """Search output parameters

    Attributes:
        facets (Union[Unset, bool]): Activate faceted search results Default: False.
        fields (Union[Unset, str]): Hit fields to be returned (e.g. 'annotations,categories' or '!text,!metadata')
        highlight (Union[Unset, bool]): Highlight query terms Default: False.
        return_hits (Union[Unset, bool]): Return hits in addition to answering the question Default: True.
    """

    facets: Union[Unset, bool] = False
    fields: Union[Unset, str] = UNSET
    highlight: Union[Unset, bool] = False
    return_hits: Union[Unset, bool] = True

    def to_dict(self) -> dict[str, Any]:
        facets = self.facets

        fields = self.fields

        highlight = self.highlight

        return_hits = self.return_hits

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if facets is not UNSET:
            field_dict["facets"] = facets
        if fields is not UNSET:
            field_dict["fields"] = fields
        if highlight is not UNSET:
            field_dict["highlight"] = highlight
        if return_hits is not UNSET:
            field_dict["returnHits"] = return_hits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        facets = d.pop("facets", UNSET)

        fields = d.pop("fields", UNSET)

        highlight = d.pop("highlight", UNSET)

        return_hits = d.pop("returnHits", UNSET)

        output_params = cls(
            facets=facets,
            fields=fields,
            highlight=highlight,
            return_hits=return_hits,
        )

        return output_params
