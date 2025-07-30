from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="OperationCount")


@_attrs_define
class OperationCount:
    """Annotation creation response

    Attributes:
        count (int): Number of elements affected by the operation
        operation (str): Name of the operation
        unit (str): Element unit of the operation
    """

    count: int
    operation: str
    unit: str

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        operation = self.operation

        unit = self.unit

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "count": count,
                "operation": operation,
                "unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        count = d.pop("count")

        operation = d.pop("operation")

        unit = d.pop("unit")

        operation_count = cls(
            count=count,
            operation=operation,
            unit=unit,
        )

        return operation_count
