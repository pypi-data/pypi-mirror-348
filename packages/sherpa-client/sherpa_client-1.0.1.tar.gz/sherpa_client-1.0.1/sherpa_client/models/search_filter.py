from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.search_filter_filter_selector import SearchFilterFilterSelector
from ..models.search_filter_filter_type import SearchFilterFilterType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchFilter")


@_attrs_define
class SearchFilter:
    """
    Attributes:
        field (Union[Unset, str]):  Default: 'text'.
        filter_selector (Union[Unset, SearchFilterFilterSelector]):  Default: SearchFilterFilterSelector.MUST.
        filter_type (Union[Unset, SearchFilterFilterType]):  Default: SearchFilterFilterType.QUERY.
        value (Union[Unset, str]): offset from the first result you want to fetch Default: ''.
    """

    field: Union[Unset, str] = "text"
    filter_selector: Union[
        Unset, SearchFilterFilterSelector
    ] = SearchFilterFilterSelector.MUST
    filter_type: Union[Unset, SearchFilterFilterType] = SearchFilterFilterType.QUERY
    value: Union[Unset, str] = ""

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        filter_selector: Union[Unset, str] = UNSET
        if not isinstance(self.filter_selector, Unset):
            filter_selector = self.filter_selector.value

        filter_type: Union[Unset, str] = UNSET
        if not isinstance(self.filter_type, Unset):
            filter_type = self.filter_type.value

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if field is not UNSET:
            field_dict["field"] = field
        if filter_selector is not UNSET:
            field_dict["filterSelector"] = filter_selector
        if filter_type is not UNSET:
            field_dict["filterType"] = filter_type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        field = d.pop("field", UNSET)

        _filter_selector = d.pop("filterSelector", UNSET)
        filter_selector: Union[Unset, SearchFilterFilterSelector]
        if isinstance(_filter_selector, Unset):
            filter_selector = UNSET
        else:
            filter_selector = SearchFilterFilterSelector(_filter_selector)

        _filter_type = d.pop("filterType", UNSET)
        filter_type: Union[Unset, SearchFilterFilterType]
        if isinstance(_filter_type, Unset):
            filter_type = UNSET
        else:
            filter_type = SearchFilterFilterType(_filter_type)

        value = d.pop("value", UNSET)

        search_filter = cls(
            field=field,
            filter_selector=filter_selector,
            filter_type=filter_type,
            value=value,
        )

        return search_filter
