from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.classification_options import ClassificationOptions


T = TypeVar("T", bound="ConfigPatchOptions")


@_attrs_define
class ConfigPatchOptions:
    """
    Attributes:
        classification (Union[Unset, ClassificationOptions]):
        clean_html (Union[Unset, bool]):
        collaborative_annotation (Union[Unset, bool]):
        created_date (Union[Unset, str]):
        description (Union[Unset, str]):
        image_filename (Union[Unset, str]):
        image_id (Union[Unset, str]):
        image_url (Union[Unset, str]):
        label (Union[Unset, str]):
        markdown_content (Union[Unset, bool]):
        metafacets (Union[Unset, list[str]]):
        replace_carriage_returns (Union[Unset, bool]):
        route_on_open_project (Union[Unset, str]):
    """

    classification: Union[Unset, "ClassificationOptions"] = UNSET
    clean_html: Union[Unset, bool] = UNSET
    collaborative_annotation: Union[Unset, bool] = UNSET
    created_date: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    image_filename: Union[Unset, str] = UNSET
    image_id: Union[Unset, str] = UNSET
    image_url: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    markdown_content: Union[Unset, bool] = UNSET
    metafacets: Union[Unset, list[str]] = UNSET
    replace_carriage_returns: Union[Unset, bool] = UNSET
    route_on_open_project: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        classification: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.classification, Unset):
            classification = self.classification.to_dict()

        clean_html = self.clean_html

        collaborative_annotation = self.collaborative_annotation

        created_date = self.created_date

        description = self.description

        image_filename = self.image_filename

        image_id = self.image_id

        image_url = self.image_url

        label = self.label

        markdown_content = self.markdown_content

        metafacets: Union[Unset, list[str]] = UNSET
        if not isinstance(self.metafacets, Unset):
            metafacets = self.metafacets

        replace_carriage_returns = self.replace_carriage_returns

        route_on_open_project = self.route_on_open_project

        field_dict: dict[str, Any] = {}
        field_dict.update({})
        if classification is not UNSET:
            field_dict["classification"] = classification
        if clean_html is not UNSET:
            field_dict["cleanHtml"] = clean_html
        if collaborative_annotation is not UNSET:
            field_dict["collaborativeAnnotation"] = collaborative_annotation
        if created_date is not UNSET:
            field_dict["createdDate"] = created_date
        if description is not UNSET:
            field_dict["description"] = description
        if image_filename is not UNSET:
            field_dict["imageFilename"] = image_filename
        if image_id is not UNSET:
            field_dict["imageId"] = image_id
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if label is not UNSET:
            field_dict["label"] = label
        if markdown_content is not UNSET:
            field_dict["markdownContent"] = markdown_content
        if metafacets is not UNSET:
            field_dict["metafacets"] = metafacets
        if replace_carriage_returns is not UNSET:
            field_dict["replaceCarriageReturns"] = replace_carriage_returns
        if route_on_open_project is not UNSET:
            field_dict["routeOnOpenProject"] = route_on_open_project

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.classification_options import ClassificationOptions

        d = dict(src_dict)
        _classification = d.pop("classification", UNSET)
        classification: Union[Unset, ClassificationOptions]
        if isinstance(_classification, Unset):
            classification = UNSET
        else:
            classification = ClassificationOptions.from_dict(_classification)

        clean_html = d.pop("cleanHtml", UNSET)

        collaborative_annotation = d.pop("collaborativeAnnotation", UNSET)

        created_date = d.pop("createdDate", UNSET)

        description = d.pop("description", UNSET)

        image_filename = d.pop("imageFilename", UNSET)

        image_id = d.pop("imageId", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        label = d.pop("label", UNSET)

        markdown_content = d.pop("markdownContent", UNSET)

        metafacets = cast(list[str], d.pop("metafacets", UNSET))

        replace_carriage_returns = d.pop("replaceCarriageReturns", UNSET)

        route_on_open_project = d.pop("routeOnOpenProject", UNSET)

        config_patch_options = cls(
            classification=classification,
            clean_html=clean_html,
            collaborative_annotation=collaborative_annotation,
            created_date=created_date,
            description=description,
            image_filename=image_filename,
            image_id=image_id,
            image_url=image_url,
            label=label,
            markdown_content=markdown_content,
            metafacets=metafacets,
            replace_carriage_returns=replace_carriage_returns,
            route_on_open_project=route_on_open_project,
        )

        return config_patch_options
