from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.project_annotators import ProjectAnnotators


T = TypeVar("T", bound="ProjectsAnnotators")


@_attrs_define
class ProjectsAnnotators:
    """
    Attributes:
        annotators (ProjectAnnotators):
        project_name (str):
    """

    annotators: "ProjectAnnotators"
    project_name: str

    def to_dict(self) -> dict[str, Any]:
        annotators = self.annotators.to_dict()

        project_name = self.project_name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "annotators": annotators,
                "projectName": project_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_annotators import ProjectAnnotators

        d = dict(src_dict)
        annotators = ProjectAnnotators.from_dict(d.pop("annotators"))

        project_name = d.pop("projectName")

        projects_annotators = cls(
            annotators=annotators,
            project_name=project_name,
        )

        return projects_annotators
