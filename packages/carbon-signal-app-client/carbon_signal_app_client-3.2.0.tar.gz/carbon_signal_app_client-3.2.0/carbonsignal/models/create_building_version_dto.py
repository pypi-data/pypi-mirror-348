from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_building_version_dto_cooling_system_type_0 import (
    CreateBuildingVersionDTOCoolingSystemType0,
    check_create_building_version_dto_cooling_system_type_0,
)
from ..models.create_building_version_dto_heating_system_type_0 import (
    CreateBuildingVersionDTOHeatingSystemType0,
    check_create_building_version_dto_heating_system_type_0,
)
from ..models.create_building_version_dto_occupancy_type_type_0 import (
    CreateBuildingVersionDTOOccupancyTypeType0,
    check_create_building_version_dto_occupancy_type_type_0,
)

if TYPE_CHECKING:
    from ..models.create_building_version_address_dto import CreateBuildingVersionAddressDTO
    from ..models.input_utility_meters import InputUtilityMeters
    from ..models.location_coordinates import LocationCoordinates


T = TypeVar("T", bound="CreateBuildingVersionDTO")


@_attrs_define
class CreateBuildingVersionDTO:
    """CreateBuildingVersionDTO.

    Attributes:
        area (float): Area of the building


            **Unit:** square feet
        heating_system (Union[CreateBuildingVersionDTOHeatingSystemType0, None]): Heating system used in the building.

            **Allowed values:**

            - `"ELECTRICITY"`
            - `"DISTRICT"`
            - `"GAS"`
            - `null` *(represents unknown)*
        cooling_system (Union[CreateBuildingVersionDTOCoolingSystemType0, None]): Cooling system used in the building.

            **Allowed values:**

            - `"ELECTRICITY"`
            - `"DISTRICT"`
            - `null` *(represents unknown)*
        measured_utilities (InputUtilityMeters): Ensures that at least one utility meter has some values.
        occupancy_type (Union[CreateBuildingVersionDTOOccupancyTypeType0, None]):
        location (Union['CreateBuildingVersionAddressDTO', 'LocationCoordinates']):
    """

    area: float
    heating_system: CreateBuildingVersionDTOHeatingSystemType0 | None
    cooling_system: CreateBuildingVersionDTOCoolingSystemType0 | None
    measured_utilities: "InputUtilityMeters"
    occupancy_type: CreateBuildingVersionDTOOccupancyTypeType0 | None
    location: Union["CreateBuildingVersionAddressDTO", "LocationCoordinates"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_building_version_address_dto import CreateBuildingVersionAddressDTO

        area = self.area

        heating_system: None | str
        heating_system = self.heating_system if isinstance(self.heating_system, str) else self.heating_system

        cooling_system: None | str
        cooling_system = self.cooling_system if isinstance(self.cooling_system, str) else self.cooling_system

        measured_utilities = self.measured_utilities.to_dict()

        occupancy_type: None | str
        occupancy_type = self.occupancy_type if isinstance(self.occupancy_type, str) else self.occupancy_type

        location: dict[str, Any]
        if isinstance(self.location, CreateBuildingVersionAddressDTO):
            location = self.location.to_dict()
        else:
            location = self.location.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "area": area,
            "heating_system": heating_system,
            "cooling_system": cooling_system,
            "measured_utilities": measured_utilities,
            "occupancy_type": occupancy_type,
            "location": location,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_building_version_address_dto import CreateBuildingVersionAddressDTO
        from ..models.input_utility_meters import InputUtilityMeters
        from ..models.location_coordinates import LocationCoordinates

        d = dict(src_dict)
        area = d.pop("area")

        def _parse_heating_system(data: object) -> CreateBuildingVersionDTOHeatingSystemType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                heating_system_type_0 = check_create_building_version_dto_heating_system_type_0(data)

                return heating_system_type_0
            except:  # noqa: E722
                pass
            return cast(CreateBuildingVersionDTOHeatingSystemType0 | None, data)

        heating_system = _parse_heating_system(d.pop("heating_system"))

        def _parse_cooling_system(data: object) -> CreateBuildingVersionDTOCoolingSystemType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cooling_system_type_0 = check_create_building_version_dto_cooling_system_type_0(data)

                return cooling_system_type_0
            except:  # noqa: E722
                pass
            return cast(CreateBuildingVersionDTOCoolingSystemType0 | None, data)

        cooling_system = _parse_cooling_system(d.pop("cooling_system"))

        measured_utilities = InputUtilityMeters.from_dict(d.pop("measured_utilities"))

        def _parse_occupancy_type(data: object) -> CreateBuildingVersionDTOOccupancyTypeType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                occupancy_type_type_0 = check_create_building_version_dto_occupancy_type_type_0(data)

                return occupancy_type_type_0
            except:  # noqa: E722
                pass
            return cast(CreateBuildingVersionDTOOccupancyTypeType0 | None, data)

        occupancy_type = _parse_occupancy_type(d.pop("occupancy_type"))

        def _parse_location(data: object) -> Union["CreateBuildingVersionAddressDTO", "LocationCoordinates"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                location_type_0 = CreateBuildingVersionAddressDTO.from_dict(data)

                return location_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            location_type_1 = LocationCoordinates.from_dict(data)

            return location_type_1

        location = _parse_location(d.pop("location"))

        create_building_version_dto = cls(
            area=area,
            heating_system=heating_system,
            cooling_system=cooling_system,
            measured_utilities=measured_utilities,
            occupancy_type=occupancy_type,
            location=location,
        )

        create_building_version_dto.additional_properties = d
        return create_building_version_dto

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
