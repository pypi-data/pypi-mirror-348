from typing import Literal, cast

BuildingCoolingSystemType0 = Literal["DISTRICT", "ELECTRICITY", "NO_SYSTEM"]

BUILDING_COOLING_SYSTEM_TYPE_0_VALUES: set[BuildingCoolingSystemType0] = {
    "DISTRICT",
    "ELECTRICITY",
    "NO_SYSTEM",
}


def check_building_cooling_system_type_0(value: str) -> BuildingCoolingSystemType0:
    if value in BUILDING_COOLING_SYSTEM_TYPE_0_VALUES:
        return cast(BuildingCoolingSystemType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BUILDING_COOLING_SYSTEM_TYPE_0_VALUES!r}")
