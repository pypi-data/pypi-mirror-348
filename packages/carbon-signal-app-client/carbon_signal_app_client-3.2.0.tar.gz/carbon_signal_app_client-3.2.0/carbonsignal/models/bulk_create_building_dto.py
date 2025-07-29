from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_building_dto import CreateBuildingDTO


T = TypeVar("T", bound="BulkCreateBuildingDTO")


@_attrs_define
class BulkCreateBuildingDTO:
    """Bulk create building DTO.

    Attributes:
        buildings (list['CreateBuildingDTO']):
    """

    buildings: list["CreateBuildingDTO"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        buildings = []
        for buildings_item_data in self.buildings:
            buildings_item = buildings_item_data.to_dict()
            buildings.append(buildings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "buildings": buildings,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_building_dto import CreateBuildingDTO

        d = dict(src_dict)
        buildings = []
        _buildings = d.pop("buildings")
        for buildings_item_data in _buildings:
            buildings_item = CreateBuildingDTO.from_dict(buildings_item_data)

            buildings.append(buildings_item)

        bulk_create_building_dto = cls(
            buildings=buildings,
        )

        bulk_create_building_dto.additional_properties = d
        return bulk_create_building_dto

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
