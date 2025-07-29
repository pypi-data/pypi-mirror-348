from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BulkTriggerBuildingsDTO")


@_attrs_define
class BulkTriggerBuildingsDTO:
    """Bulk trigger interventions DTO.

    Attributes:
        building_ids (list[int]):
    """

    building_ids: list[int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        building_ids = self.building_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "building_ids": building_ids,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        building_ids = cast(list[int], d.pop("building_ids"))

        bulk_trigger_buildings_dto = cls(
            building_ids=building_ids,
        )

        bulk_trigger_buildings_dto.additional_properties = d
        return bulk_trigger_buildings_dto

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
