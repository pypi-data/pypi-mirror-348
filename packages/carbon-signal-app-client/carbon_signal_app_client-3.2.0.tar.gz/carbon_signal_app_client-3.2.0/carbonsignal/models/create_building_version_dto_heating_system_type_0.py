from typing import Literal, cast

CreateBuildingVersionDTOHeatingSystemType0 = Literal["DISTRICT", "ELECTRICITY", "GAS", "NO_SYSTEM"]

CREATE_BUILDING_VERSION_DTO_HEATING_SYSTEM_TYPE_0_VALUES: set[CreateBuildingVersionDTOHeatingSystemType0] = {
    "DISTRICT",
    "ELECTRICITY",
    "GAS",
    "NO_SYSTEM",
}


def check_create_building_version_dto_heating_system_type_0(value: str) -> CreateBuildingVersionDTOHeatingSystemType0:
    if value in CREATE_BUILDING_VERSION_DTO_HEATING_SYSTEM_TYPE_0_VALUES:
        return cast(CreateBuildingVersionDTOHeatingSystemType0, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREATE_BUILDING_VERSION_DTO_HEATING_SYSTEM_TYPE_0_VALUES!r}"
    )
