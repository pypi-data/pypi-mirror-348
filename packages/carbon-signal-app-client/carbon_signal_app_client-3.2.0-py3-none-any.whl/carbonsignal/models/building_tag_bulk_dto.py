from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.building_tag_bulk_dto_action import BuildingTagBulkDTOAction, check_building_tag_bulk_dto_action

T = TypeVar("T", bound="BuildingTagBulkDTO")


@_attrs_define
class BuildingTagBulkDTO:
    """Single Bulk Tag DTO.

    Attributes:
        tag_id (int):
        action (BuildingTagBulkDTOAction):
        building_id (int):
    """

    tag_id: int
    action: BuildingTagBulkDTOAction
    building_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        tag_id = self.tag_id

        action: str = self.action

        building_id = self.building_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "tag_id": tag_id,
            "action": action,
            "building_id": building_id,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tag_id = d.pop("tag_id")

        action = check_building_tag_bulk_dto_action(d.pop("action"))

        building_id = d.pop("building_id")

        building_tag_bulk_dto = cls(
            tag_id=tag_id,
            action=action,
            building_id=building_id,
        )

        building_tag_bulk_dto.additional_properties = d
        return building_tag_bulk_dto

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
