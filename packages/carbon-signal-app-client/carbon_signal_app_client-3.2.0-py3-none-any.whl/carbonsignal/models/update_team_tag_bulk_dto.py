from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_team_tag_bulk_dto_color import UpdateTeamTagBulkDTOColor, check_update_team_tag_bulk_dto_color

T = TypeVar("T", bound="UpdateTeamTagBulkDTO")


@_attrs_define
class UpdateTeamTagBulkDTO:
    """Single Bulk Tag Put DTO.

    Attributes:
        name (str):
        color (UpdateTeamTagBulkDTOColor):
        action (Literal['PUT']):
        tag_id (int):
    """

    name: str
    color: UpdateTeamTagBulkDTOColor
    action: Literal["PUT"]
    tag_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        color: str = self.color

        action = self.action

        tag_id = self.tag_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "color": color,
            "action": action,
            "tag_id": tag_id,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        color = check_update_team_tag_bulk_dto_color(d.pop("color"))

        action = cast(Literal["PUT"], d.pop("action"))
        if action != "PUT":
            raise ValueError(f"action must match const 'PUT', got '{action}'")

        tag_id = d.pop("tag_id")

        update_team_tag_bulk_dto = cls(
            name=name,
            color=color,
            action=action,
            tag_id=tag_id,
        )

        update_team_tag_bulk_dto.additional_properties = d
        return update_team_tag_bulk_dto

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
