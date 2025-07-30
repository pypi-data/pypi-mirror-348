from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.message_patch_template import MessagePatchTemplate
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.message_audience import MessageAudience
    from ..models.message_patch_localized import MessagePatchLocalized


T = TypeVar("T", bound="MessagePatch")


@_attrs_define
class MessagePatch:
    """
    Attributes:
        localized (MessagePatchLocalized):
        audience (Union[Unset, MessageAudience]):
        group (Union[Unset, str]):
        index (Union[Unset, int]):
        scope (Union[Unset, str]):
        template (Union[Unset, MessagePatchTemplate]):
    """

    localized: "MessagePatchLocalized"
    audience: Union[Unset, "MessageAudience"] = UNSET
    group: Union[Unset, str] = UNSET
    index: Union[Unset, int] = UNSET
    scope: Union[Unset, str] = UNSET
    template: Union[Unset, MessagePatchTemplate] = UNSET

    def to_dict(self) -> dict[str, Any]:
        localized = self.localized.to_dict()

        audience: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.audience, Unset):
            audience = self.audience.to_dict()

        group = self.group

        index = self.index

        scope = self.scope

        template: Union[Unset, str] = UNSET
        if not isinstance(self.template, Unset):
            template = self.template.value

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "localized": localized,
            }
        )
        if audience is not UNSET:
            field_dict["audience"] = audience
        if group is not UNSET:
            field_dict["group"] = group
        if index is not UNSET:
            field_dict["index"] = index
        if scope is not UNSET:
            field_dict["scope"] = scope
        if template is not UNSET:
            field_dict["template"] = template

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.message_audience import MessageAudience
        from ..models.message_patch_localized import MessagePatchLocalized

        d = dict(src_dict)
        localized = MessagePatchLocalized.from_dict(d.pop("localized"))

        _audience = d.pop("audience", UNSET)
        audience: Union[Unset, MessageAudience]
        if isinstance(_audience, Unset):
            audience = UNSET
        else:
            audience = MessageAudience.from_dict(_audience)

        group = d.pop("group", UNSET)

        index = d.pop("index", UNSET)

        scope = d.pop("scope", UNSET)

        _template = d.pop("template", UNSET)
        template: Union[Unset, MessagePatchTemplate]
        if isinstance(_template, Unset):
            template = UNSET
        else:
            template = MessagePatchTemplate(_template)

        message_patch = cls(
            localized=localized,
            audience=audience,
            group=group,
            index=index,
            scope=scope,
            template=template,
        )

        return message_patch
