from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.search_filter import SearchFilter


T = TypeVar("T", bound="FilteringParams")


@_attrs_define
class FilteringParams:
    """Filtering parameters

    Attributes:
        filters (Union[Unset, list['SearchFilter']]):
        query_filter (Union[Unset, str]): Optional Lucene query string to filter on, e.g.: '+annotations:*'
        selected_facets (Union[Unset, list[str]]):
    """

    filters: Union[Unset, list["SearchFilter"]] = UNSET
    query_filter: Union[Unset, str] = UNSET
    selected_facets: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)

        query_filter = self.query_filter

        selected_facets: Union[Unset, list[str]] = UNSET
        if not isinstance(self.selected_facets, Unset):
            selected_facets = self.selected_facets

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters
        if query_filter is not UNSET:
            field_dict["queryFilter"] = query_filter
        if selected_facets is not UNSET:
            field_dict["selectedFacets"] = selected_facets

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.search_filter import SearchFilter

        d = dict(src_dict)
        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:
            filters_item = SearchFilter.from_dict(filters_item_data)

            filters.append(filters_item)

        query_filter = d.pop("queryFilter", UNSET)

        selected_facets = cast(list[str], d.pop("selectedFacets", UNSET))

        filtering_params = cls(
            filters=filters,
            query_filter=query_filter,
            selected_facets=selected_facets,
        )

        return filtering_params
