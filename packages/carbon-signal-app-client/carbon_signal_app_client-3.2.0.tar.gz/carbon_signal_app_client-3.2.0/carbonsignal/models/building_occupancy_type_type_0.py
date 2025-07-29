from typing import Literal, cast

BuildingOccupancyTypeType0 = Literal[
    "DATA_CENTER",
    "ENCLOSED_MALL",
    "HOSPITAL",
    "HOTEL",
    "LABORATORY",
    "MEDICAL_OFFICE",
    "MEETING_HALL",
    "MF_HOUSING",
    "MIXED",
    "NON_REFRIGERATED_WAREHOUSE",
    "OFFICE",
    "OTHER_PUBLIC_SERVICES",
    "OTHER_RESIDENTIAL",
    "PLANT",
    "REFRIGERATED_WAREHOUSE",
    "RESTAURANT",
    "RETAIL",
    "SCHOOL",
    "SUPERMARKET",
    "UNIVERSITY",
    "WHOLESALE_CLUB",
]

BUILDING_OCCUPANCY_TYPE_TYPE_0_VALUES: set[BuildingOccupancyTypeType0] = {
    "DATA_CENTER",
    "ENCLOSED_MALL",
    "HOSPITAL",
    "HOTEL",
    "LABORATORY",
    "MEDICAL_OFFICE",
    "MEETING_HALL",
    "MF_HOUSING",
    "MIXED",
    "NON_REFRIGERATED_WAREHOUSE",
    "OFFICE",
    "OTHER_PUBLIC_SERVICES",
    "OTHER_RESIDENTIAL",
    "PLANT",
    "REFRIGERATED_WAREHOUSE",
    "RESTAURANT",
    "RETAIL",
    "SCHOOL",
    "SUPERMARKET",
    "UNIVERSITY",
    "WHOLESALE_CLUB",
}


def check_building_occupancy_type_type_0(value: str) -> BuildingOccupancyTypeType0:
    if value in BUILDING_OCCUPANCY_TYPE_TYPE_0_VALUES:
        return cast(BuildingOccupancyTypeType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BUILDING_OCCUPANCY_TYPE_TYPE_0_VALUES!r}")
