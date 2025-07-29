from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_building_inspector_dto import CreateBuildingInspectorDTO
    from ..models.inspection_message import InspectionMessage


T = TypeVar("T", bound="InspectedBuilding")


@_attrs_define
class InspectedBuilding:
    """
    Attributes:
        building_entity (CreateBuildingInspectorDTO): CreateBuildingInspectorDTO.
        warnings (list['InspectionMessage']):
    """

    building_entity: "CreateBuildingInspectorDTO"
    warnings: list["InspectionMessage"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        building_entity = self.building_entity.to_dict()

        warnings = []
        for warnings_item_data in self.warnings:
            warnings_item = warnings_item_data.to_dict()
            warnings.append(warnings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "buildingEntity": building_entity,
            "warnings": warnings,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_building_inspector_dto import CreateBuildingInspectorDTO
        from ..models.inspection_message import InspectionMessage

        d = dict(src_dict)
        building_entity = CreateBuildingInspectorDTO.from_dict(d.pop("buildingEntity"))

        warnings = []
        _warnings = d.pop("warnings")
        for warnings_item_data in _warnings:
            warnings_item = InspectionMessage.from_dict(warnings_item_data)

            warnings.append(warnings_item)

        inspected_building = cls(
            building_entity=building_entity,
            warnings=warnings,
        )

        inspected_building.additional_properties = d
        return inspected_building

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
