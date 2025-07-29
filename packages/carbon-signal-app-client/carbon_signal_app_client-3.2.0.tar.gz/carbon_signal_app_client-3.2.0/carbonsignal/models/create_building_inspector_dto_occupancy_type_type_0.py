from typing import Literal, cast

CreateBuildingInspectorDTOOccupancyTypeType0 = Literal[
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

CREATE_BUILDING_INSPECTOR_DTO_OCCUPANCY_TYPE_TYPE_0_VALUES: set[CreateBuildingInspectorDTOOccupancyTypeType0] = {
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


def check_create_building_inspector_dto_occupancy_type_type_0(
    value: str,
) -> CreateBuildingInspectorDTOOccupancyTypeType0:
    if value in CREATE_BUILDING_INSPECTOR_DTO_OCCUPANCY_TYPE_TYPE_0_VALUES:
        return cast(CreateBuildingInspectorDTOOccupancyTypeType0, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREATE_BUILDING_INSPECTOR_DTO_OCCUPANCY_TYPE_TYPE_0_VALUES!r}"
    )
