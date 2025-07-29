from typing import Literal, cast

BuildingHeatingSystemType0 = Literal["DISTRICT", "ELECTRICITY", "GAS", "NO_SYSTEM"]

BUILDING_HEATING_SYSTEM_TYPE_0_VALUES: set[BuildingHeatingSystemType0] = {
    "DISTRICT",
    "ELECTRICITY",
    "GAS",
    "NO_SYSTEM",
}


def check_building_heating_system_type_0(value: str) -> BuildingHeatingSystemType0:
    if value in BUILDING_HEATING_SYSTEM_TYPE_0_VALUES:
        return cast(BuildingHeatingSystemType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BUILDING_HEATING_SYSTEM_TYPE_0_VALUES!r}")
