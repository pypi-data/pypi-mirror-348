from typing import Literal, cast

CreateBuildingDTOHeatingSystemType0 = Literal["DISTRICT", "ELECTRICITY", "GAS", "NO_SYSTEM"]

CREATE_BUILDING_DTO_HEATING_SYSTEM_TYPE_0_VALUES: set[CreateBuildingDTOHeatingSystemType0] = {
    "DISTRICT",
    "ELECTRICITY",
    "GAS",
    "NO_SYSTEM",
}


def check_create_building_dto_heating_system_type_0(value: str) -> CreateBuildingDTOHeatingSystemType0:
    if value in CREATE_BUILDING_DTO_HEATING_SYSTEM_TYPE_0_VALUES:
        return cast(CreateBuildingDTOHeatingSystemType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_BUILDING_DTO_HEATING_SYSTEM_TYPE_0_VALUES!r}")
