from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.building_cooling_system_type_0 import BuildingCoolingSystemType0, check_building_cooling_system_type_0
from ..models.building_heating_system_type_0 import BuildingHeatingSystemType0, check_building_heating_system_type_0
from ..models.building_occupancy_type_type_0 import BuildingOccupancyTypeType0, check_building_occupancy_type_type_0
from ..models.building_status import BuildingStatus, check_building_status

if TYPE_CHECKING:
    from ..models.adjusted_utility_meters import AdjustedUtilityMeters
    from ..models.building_version import BuildingVersion
    from ..models.emission_factors import EmissionFactors
    from ..models.emissions_intensities import EmissionsIntensities
    from ..models.energy_use_intensities import EnergyUseIntensities
    from ..models.location_address import LocationAddress
    from ..models.location_coordinates import LocationCoordinates
    from ..models.utility_meters import UtilityMeters


T = TypeVar("T", bound="Building")


@_attrs_define
class Building:
    """Building.

    Attributes:
        id (int):
        name (str): Name of the building.
        area (float): Area of the building


            **Unit:** square feet
        location (Union['LocationAddress', 'LocationCoordinates']):
        heating_system (Union[BuildingHeatingSystemType0, None]): Heating system used in the building.

            **Allowed values:**

            - `"ELECTRICITY"`
            - `"DISTRICT"`
            - `"GAS"`
            - `null` *(represents unknown)*
        cooling_system (Union[BuildingCoolingSystemType0, None]): Cooling system used in the building.

            **Allowed values:**

            - `"ELECTRICITY"`
            - `"DISTRICT"`
            - `null` *(represents unknown)*
        emission_factors (EmissionFactors): EmissionFactors.
        measured_utilities (UtilityMeters): UtilityMeters.
        adjusted_measured_utilities (AdjustedUtilityMeters): AdjustedUtilityMeters.
        is_gap_filling_allowed (bool): Is gap filling enabled for the building?  If true, then gap filling can be used
            to fill in missing data where detected.
        energy_intensity (EnergyUseIntensities): EnergyUseIntensities.
        emissions_intensity (EmissionsIntensities): EmissionsIntensities.
        notes (Union[None, str]): User notes saved on the building.
        tag_ids (list[int]): Tag IDs associated with the building.

            **Note:** this field is primarily for internal use only.
        active_version_id (int): The ID of the active building version used to generate other building details.

            **Note:** this field is primarily for internal use only.
        versions (list['BuildingVersion']): List of current and old building versions.

            **Note:** this field is primarily for internal use only.
        occupancy_type (Union[BuildingOccupancyTypeType0, None]): Occupancy type of the building.  Choose the primary
            type if multiple.

            **Allowed values:**

            - `"OFFICE"`
            - `"UNIVERSITY"`
            - `"SCHOOL"`
            - `"RESTAURANT"`
            - `"HOSPITAL"`
            - `"MEDICAL_OFFICE"`
            - `"HOTEL"`
            - `"MF_HOUSING"`
            - `"OTHER_RESIDENTIAL"`
            - `"PLANT"`
            - `"MIXED"`
            - `"MEETING_HALL"`
            - `"OTHER_PUBLIC_SERVICES"`
            - `"ENCLOSED_MALL"`
            - `"RETAIL"`
            - `"SUPERMARKET"`
            - `"WHOLESALE_CLUB"`
            - `"LABORATORY"`
            - `"DATA_CENTER"`
            - `"REFRIGERATED_WAREHOUSE"`
            - `"NON_REFRIGERATED_WAREHOUSE"`
            - `null` *(represents unknown)*
        status (BuildingStatus): Status of the buildings calibration and its strategies.

            **Options:**

            - `NOT_STARTED`
            - `QUEUED_BASELINE`
            - `RUNNING_BASELINE`
            - `FAILED_BASELINE`
            - `DRAFT`
            - `QUEUED_STRATEGIES`
            - `RUNNING_STRATEGIES`
            - `FAILED_STRATEGIES`
            - `COMPLETED`
    """

    id: int
    name: str
    area: float
    location: Union["LocationAddress", "LocationCoordinates"]
    heating_system: BuildingHeatingSystemType0 | None
    cooling_system: BuildingCoolingSystemType0 | None
    emission_factors: "EmissionFactors"
    measured_utilities: "UtilityMeters"
    adjusted_measured_utilities: "AdjustedUtilityMeters"
    is_gap_filling_allowed: bool
    energy_intensity: "EnergyUseIntensities"
    emissions_intensity: "EmissionsIntensities"
    notes: None | str
    tag_ids: list[int]
    active_version_id: int
    versions: list["BuildingVersion"]
    occupancy_type: BuildingOccupancyTypeType0 | None
    status: BuildingStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.location_address import LocationAddress

        id = self.id

        name = self.name

        area = self.area

        location: dict[str, Any]
        location = self.location.to_dict() if isinstance(self.location, LocationAddress) else self.location.to_dict()

        heating_system: None | str
        heating_system = self.heating_system if isinstance(self.heating_system, str) else self.heating_system

        cooling_system: None | str
        cooling_system = self.cooling_system if isinstance(self.cooling_system, str) else self.cooling_system

        emission_factors = self.emission_factors.to_dict()

        measured_utilities = self.measured_utilities.to_dict()

        adjusted_measured_utilities = self.adjusted_measured_utilities.to_dict()

        is_gap_filling_allowed = self.is_gap_filling_allowed

        energy_intensity = self.energy_intensity.to_dict()

        emissions_intensity = self.emissions_intensity.to_dict()

        notes: None | str
        notes = self.notes

        tag_ids = self.tag_ids

        active_version_id = self.active_version_id

        versions = []
        for versions_item_data in self.versions:
            versions_item = versions_item_data.to_dict()
            versions.append(versions_item)

        occupancy_type: None | str
        occupancy_type = self.occupancy_type if isinstance(self.occupancy_type, str) else self.occupancy_type

        status: str = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "area": area,
            "location": location,
            "heating_system": heating_system,
            "cooling_system": cooling_system,
            "emission_factors": emission_factors,
            "measured_utilities": measured_utilities,
            "adjusted_measured_utilities": adjusted_measured_utilities,
            "is_gap_filling_allowed": is_gap_filling_allowed,
            "energy_intensity": energy_intensity,
            "emissions_intensity": emissions_intensity,
            "notes": notes,
            "tag_ids": tag_ids,
            "active_version_id": active_version_id,
            "versions": versions,
            "occupancy_type": occupancy_type,
            "status": status,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.adjusted_utility_meters import AdjustedUtilityMeters
        from ..models.building_version import BuildingVersion
        from ..models.emission_factors import EmissionFactors
        from ..models.emissions_intensities import EmissionsIntensities
        from ..models.energy_use_intensities import EnergyUseIntensities
        from ..models.location_address import LocationAddress
        from ..models.location_coordinates import LocationCoordinates
        from ..models.utility_meters import UtilityMeters

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        area = d.pop("area")

        def _parse_location(data: object) -> Union["LocationAddress", "LocationCoordinates"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                location_type_0 = LocationAddress.from_dict(data)

                return location_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            location_type_1 = LocationCoordinates.from_dict(data)

            return location_type_1

        location = _parse_location(d.pop("location"))

        def _parse_heating_system(data: object) -> BuildingHeatingSystemType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                heating_system_type_0 = check_building_heating_system_type_0(data)

                return heating_system_type_0
            except:  # noqa: E722
                pass
            return cast(BuildingHeatingSystemType0 | None, data)

        heating_system = _parse_heating_system(d.pop("heating_system"))

        def _parse_cooling_system(data: object) -> BuildingCoolingSystemType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                cooling_system_type_0 = check_building_cooling_system_type_0(data)

                return cooling_system_type_0
            except:  # noqa: E722
                pass
            return cast(BuildingCoolingSystemType0 | None, data)

        cooling_system = _parse_cooling_system(d.pop("cooling_system"))

        emission_factors = EmissionFactors.from_dict(d.pop("emission_factors"))

        measured_utilities = UtilityMeters.from_dict(d.pop("measured_utilities"))

        adjusted_measured_utilities = AdjustedUtilityMeters.from_dict(d.pop("adjusted_measured_utilities"))

        is_gap_filling_allowed = d.pop("is_gap_filling_allowed")

        energy_intensity = EnergyUseIntensities.from_dict(d.pop("energy_intensity"))

        emissions_intensity = EmissionsIntensities.from_dict(d.pop("emissions_intensity"))

        def _parse_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        notes = _parse_notes(d.pop("notes"))

        tag_ids = cast(list[int], d.pop("tag_ids"))

        active_version_id = d.pop("active_version_id")

        versions = []
        _versions = d.pop("versions")
        for versions_item_data in _versions:
            versions_item = BuildingVersion.from_dict(versions_item_data)

            versions.append(versions_item)

        def _parse_occupancy_type(data: object) -> BuildingOccupancyTypeType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                occupancy_type_type_0 = check_building_occupancy_type_type_0(data)

                return occupancy_type_type_0
            except:  # noqa: E722
                pass
            return cast(BuildingOccupancyTypeType0 | None, data)

        occupancy_type = _parse_occupancy_type(d.pop("occupancy_type"))

        status = check_building_status(d.pop("status"))

        building = cls(
            id=id,
            name=name,
            area=area,
            location=location,
            heating_system=heating_system,
            cooling_system=cooling_system,
            emission_factors=emission_factors,
            measured_utilities=measured_utilities,
            adjusted_measured_utilities=adjusted_measured_utilities,
            is_gap_filling_allowed=is_gap_filling_allowed,
            energy_intensity=energy_intensity,
            emissions_intensity=emissions_intensity,
            notes=notes,
            tag_ids=tag_ids,
            active_version_id=active_version_id,
            versions=versions,
            occupancy_type=occupancy_type,
            status=status,
        )

        building.additional_properties = d
        return building

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
