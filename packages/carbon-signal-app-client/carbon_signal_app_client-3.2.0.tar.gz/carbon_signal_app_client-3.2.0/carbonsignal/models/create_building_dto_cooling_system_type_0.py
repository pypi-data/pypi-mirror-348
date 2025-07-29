from typing import Literal, cast

CreateBuildingDTOCoolingSystemType0 = Literal["DISTRICT", "ELECTRICITY", "NO_SYSTEM"]

CREATE_BUILDING_DTO_COOLING_SYSTEM_TYPE_0_VALUES: set[CreateBuildingDTOCoolingSystemType0] = {
    "DISTRICT",
    "ELECTRICITY",
    "NO_SYSTEM",
}


def check_create_building_dto_cooling_system_type_0(value: str) -> CreateBuildingDTOCoolingSystemType0:
    if value in CREATE_BUILDING_DTO_COOLING_SYSTEM_TYPE_0_VALUES:
        return cast(CreateBuildingDTOCoolingSystemType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_BUILDING_DTO_COOLING_SYSTEM_TYPE_0_VALUES!r}")
