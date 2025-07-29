from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeleteTeamTagBulkDTO")


@_attrs_define
class DeleteTeamTagBulkDTO:
    """Single Bulk Tag Delete DTO.

    Attributes:
        action (Literal['DELETE']):
        tag_id (int):
    """

    action: Literal["DELETE"]
    tag_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action

        tag_id = self.tag_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "action": action,
            "tag_id": tag_id,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        action = cast(Literal["DELETE"], d.pop("action"))
        if action != "DELETE":
            raise ValueError(f"action must match const 'DELETE', got '{action}'")

        tag_id = d.pop("tag_id")

        delete_team_tag_bulk_dto = cls(
            action=action,
            tag_id=tag_id,
        )

        delete_team_tag_bulk_dto.additional_properties = d
        return delete_team_tag_bulk_dto

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
