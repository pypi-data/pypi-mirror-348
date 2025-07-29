from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.tag_color import TagColor, check_tag_color

T = TypeVar("T", bound="Tag")


@_attrs_define
class Tag:
    """Tag schema.

    Attributes:
        id (int):
        name (str):
        team_id (int):
        color (TagColor):
    """

    id: int
    name: str
    team_id: int
    color: TagColor
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        team_id = self.team_id

        color: str = self.color

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "team_id": team_id,
            "color": color,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        team_id = d.pop("team_id")

        color = check_tag_color(d.pop("color"))

        tag = cls(
            id=id,
            name=name,
            team_id=team_id,
            color=color,
        )

        tag.additional_properties = d
        return tag

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
