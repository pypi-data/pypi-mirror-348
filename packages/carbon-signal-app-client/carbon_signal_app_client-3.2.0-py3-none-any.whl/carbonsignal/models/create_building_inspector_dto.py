from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_building_inspector_dto_cooling_system_type_0 import (
    CreateBuildingInspectorDTOCoolingSystemType0,
    check_create_building_inspector_dto_cooling_system_type_0,
)
from ..models.create_building_inspector_dto_heating_system_type_0 import (
    CreateBuildingInspectorDTOHeatingSystemType0,
    check_create_building_inspector_dto_heating_system_type_0,
)
from ..models.create_building_inspector_dto_occupancy_type_type_0 import (
    CreateBuildingInspectorDTOOccupancyTypeType0,
    check_create_building_inspector_dto_occupancy_type_type_0,
)

if TYPE_CHECKING:
    from ..models.create_building_version_address_inspector_dto import CreateBuildingVersionAddressInspectorDTO
    from ..models.location_coordinates import LocationCoordinates
    from ..models.tag_dto import TagDTO
    from ..models.update_emission_factors_dto import UpdateEmissionFactorsDTO
    from ..models.utility_meters import UtilityMeters


T = TypeVar("T", bound="CreateBuildingInspectorDTO")


@_attrs_define
class CreateBuildingInspectorDTO:
    """CreateBuildingInspectorDTO.

    Attributes:
        area (Union[None, float]):
        heating_system (Union[CreateBuildingInspectorDTOHeatingSystemType0, None]): Heating system used in the building.

            **Allowed values:**

            - `"ELECTRICITY"`
            - `"DISTRICT"`
            - `"GAS"`
            - `null` *(represents unknown)*
        cooling_system (Union[CreateBuildingInspectorDTOCoolingSystemType0, None]): Cooling system used in the building.

            **Allowed values:**

            - `"ELECTRICITY"`
            - `"DISTRICT"`
            - `null` *(represents unknown)*
        measured_utilities (UtilityMeters): UtilityMeters.
        occupancy_type (Union[CreateBuildingInspectorDTOOccupancyTypeType0, None]):
        location (Union['CreateBuildingVersionAddressInspectorDTO', 'LocationCoordinates']):
        name (str): Name of the building.
        notes (Union[None, str]):
        emission_factors (UpdateEmissionFactorsDTO): UpdateEmissionFactors.
        tags (list['TagDTO']):
    """

    area: None | float
    heating_system: CreateBuildingInspectorDTOHeatingSystemType0 | None
    cooling_system: CreateBuildingInspectorDTOCoolingSystemType0 | None
    measured_utilities: "UtilityMeters"
    occupancy_type: CreateBuildingInspectorDTOOccupancyTypeType0 | None
    location: Union["CreateBuildingVersionAddressInspectorDTO", "LocationCoordinates"]
    name: str
    notes: None | str
    emission_factors: "UpdateEmissionFactorsDTO"
    tags: list["TagDTO"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_building_version_address_inspector_dto import CreateBuildingVersionAddressInspectorDTO

        area: None | float
        area = self.area

        heating_system: None | str
        heating_system = self.heating_system if isinstance(self.heating_system, str) else self.heating_system

        cooling_system: None | str
        cooling_system = self.cooling_system if isinstance(self.cooling_system, str) else self.cooling_system

        measured_utilities = self.measured_utilities.to_dict()

        occupancy_type: None | str
        occupancy_type = self.occupancy_type if isinstance(self.occupancy_type, str) else self.occupancy_type

        location: dict[str, Any]
        if isinstance(self.location, CreateBuildingVersionAddressInspectorDTO):
            location = self.location.to_dict()
        else:
            location = self.location.to_dict()

        name = self.name

        notes: None | str
        notes = self.notes

        emission_factors = self.emission_factors.to_dict()

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "area": area,
            "heating_system": heating_system,
            "cooling_system": cooling_system,
            "measured_utilities": measured_utilities,
            "occupancy_type": occupancy_type,
            "location": location,
            "name": name,
            "notes": notes,
            "emission_factors": emission_factors,
            "tags": tags,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_building_version_address_inspector_dto import CreateBuildingVersionAddressInspectorDTO
        from ..models.location_coordinates import LocationCoordinates
        from ..models.tag_dto import TagDTO
        from ..models.update_emission_factors_dto import UpdateEmissionFactorsDTO
        from ..models.utility_meters import UtilityMeters

        d = dict(src_dict)

        def _parse_area(data: object) -> None | float:
            if data is None:
                return data
            return cast(None | float, data)

        area = _parse_area(d.pop("area"))

        def _parse_heating_system(data: object) -> CreateBuildingInspectorDTOHeatingSystemType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                heating_system_type_0 = check_create_building_inspector_dto_heating_system_type_0(data)

                return heating_system_type_0
            except:  # noqa: E722
                pass
            return cast(CreateBuildingInspectorDTOHeatingSystemType0 | None, data)

        heating_system = _parse_heating_system(d.pop("heating_system"))

        def _parse_cooling_system(data: object) -> CreateBuildingInspectorDTOCoolingSystemType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cooling_system_type_0 = check_create_building_inspector_dto_cooling_system_type_0(data)

                return cooling_system_type_0
            except:  # noqa: E722
                pass
            return cast(CreateBuildingInspectorDTOCoolingSystemType0 | None, data)

        cooling_system = _parse_cooling_system(d.pop("cooling_system"))

        measured_utilities = UtilityMeters.from_dict(d.pop("measured_utilities"))

        def _parse_occupancy_type(data: object) -> CreateBuildingInspectorDTOOccupancyTypeType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                occupancy_type_type_0 = check_create_building_inspector_dto_occupancy_type_type_0(data)

                return occupancy_type_type_0
            except:  # noqa: E722
                pass
            return cast(CreateBuildingInspectorDTOOccupancyTypeType0 | None, data)

        occupancy_type = _parse_occupancy_type(d.pop("occupancy_type"))

        def _parse_location(data: object) -> Union["CreateBuildingVersionAddressInspectorDTO", "LocationCoordinates"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                location_type_0 = CreateBuildingVersionAddressInspectorDTO.from_dict(data)

                return location_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            location_type_1 = LocationCoordinates.from_dict(data)

            return location_type_1

        location = _parse_location(d.pop("location"))

        name = d.pop("name")

        def _parse_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        notes = _parse_notes(d.pop("notes"))

        emission_factors = UpdateEmissionFactorsDTO.from_dict(d.pop("emission_factors"))

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = TagDTO.from_dict(tags_item_data)

            tags.append(tags_item)

        create_building_inspector_dto = cls(
            area=area,
            heating_system=heating_system,
            cooling_system=cooling_system,
            measured_utilities=measured_utilities,
            occupancy_type=occupancy_type,
            location=location,
            name=name,
            notes=notes,
            emission_factors=emission_factors,
            tags=tags,
        )

        create_building_inspector_dto.additional_properties = d
        return create_building_inspector_dto

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
