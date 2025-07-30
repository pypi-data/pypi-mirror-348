from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.segmenter_parameters import SegmenterParameters


T = TypeVar("T", bound="Segmenter")


@attr.s(auto_attribs=True)
class Segmenter:
    """
    Attributes:
        name (str): Name of the segmenter (e.g. blingfire) or name of the conversion plan
        parameters (Union[Unset, SegmenterParameters]): Optional conversion parameters
        project_name (Union[Unset, str]): If conversion plan, name of the project containing the plan
    """

    name: str
    parameters: Union[Unset, "SegmenterParameters"] = UNSET
    project_name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        parameters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict()

        project_name = self.project_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if project_name is not UNSET:
            field_dict["projectName"] = project_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.segmenter_parameters import SegmenterParameters

        d = src_dict.copy()
        name = d.pop("name")

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, SegmenterParameters]
        if isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = SegmenterParameters.from_dict(_parameters)

        project_name = d.pop("projectName", UNSET)

        segmenter = cls(
            name=name,
            parameters=parameters,
            project_name=project_name,
        )

        return segmenter
