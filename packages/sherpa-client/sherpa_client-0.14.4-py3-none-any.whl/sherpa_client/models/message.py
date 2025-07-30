from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar, Union

import attr

from ..models.message_template import MessageTemplate
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.message_audience import MessageAudience
    from ..models.message_localized import MessageLocalized
    from ..models.message_mark import MessageMark


T = TypeVar("T", bound="Message")


@attr.s(auto_attribs=True)
class Message:
    """
    Attributes:
        id (str):
        localized (MessageLocalized):
        audience (Union[Unset, MessageAudience]):
        group (Union[Unset, str]):
        index (Union[Unset, int]):
        mark (Union[Unset, MessageMark]):
        template (Union[Unset, MessageTemplate]):
    """

    id: str
    localized: "MessageLocalized"
    audience: Union[Unset, "MessageAudience"] = UNSET
    group: Union[Unset, str] = UNSET
    index: Union[Unset, int] = UNSET
    mark: Union[Unset, "MessageMark"] = UNSET
    template: Union[Unset, MessageTemplate] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        localized = self.localized.to_dict()

        audience: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.audience, Unset):
            audience = self.audience.to_dict()

        group = self.group
        index = self.index
        mark: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mark, Unset):
            mark = self.mark.to_dict()

        template: Union[Unset, str] = UNSET
        if not isinstance(self.template, Unset):
            template = self.template.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "localized": localized,
            }
        )
        if audience is not UNSET:
            field_dict["audience"] = audience
        if group is not UNSET:
            field_dict["group"] = group
        if index is not UNSET:
            field_dict["index"] = index
        if mark is not UNSET:
            field_dict["mark"] = mark
        if template is not UNSET:
            field_dict["template"] = template

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.message_audience import MessageAudience
        from ..models.message_localized import MessageLocalized
        from ..models.message_mark import MessageMark

        d = src_dict.copy()
        id = d.pop("id")

        localized = MessageLocalized.from_dict(d.pop("localized"))

        _audience = d.pop("audience", UNSET)
        audience: Union[Unset, MessageAudience]
        if isinstance(_audience, Unset):
            audience = UNSET
        else:
            audience = MessageAudience.from_dict(_audience)

        group = d.pop("group", UNSET)

        index = d.pop("index", UNSET)

        _mark = d.pop("mark", UNSET)
        mark: Union[Unset, MessageMark]
        if isinstance(_mark, Unset):
            mark = UNSET
        else:
            mark = MessageMark.from_dict(_mark)

        _template = d.pop("template", UNSET)
        template: Union[Unset, MessageTemplate]
        if isinstance(_template, Unset):
            template = UNSET
        else:
            template = MessageTemplate(_template)

        message = cls(
            id=id,
            localized=localized,
            audience=audience,
            group=group,
            index=index,
            mark=mark,
            template=template,
        )

        return message
