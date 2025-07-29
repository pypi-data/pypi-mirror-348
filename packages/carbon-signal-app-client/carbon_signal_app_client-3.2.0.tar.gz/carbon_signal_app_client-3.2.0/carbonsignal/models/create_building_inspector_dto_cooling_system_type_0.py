from typing import Literal, cast

CreateBuildingInspectorDTOCoolingSystemType0 = Literal["DISTRICT", "ELECTRICITY", "NO_SYSTEM"]

CREATE_BUILDING_INSPECTOR_DTO_COOLING_SYSTEM_TYPE_0_VALUES: set[CreateBuildingInspectorDTOCoolingSystemType0] = {
    "DISTRICT",
    "ELECTRICITY",
    "NO_SYSTEM",
}


def check_create_building_inspector_dto_cooling_system_type_0(
    value: str,
) -> CreateBuildingInspectorDTOCoolingSystemType0:
    if value in CREATE_BUILDING_INSPECTOR_DTO_COOLING_SYSTEM_TYPE_0_VALUES:
        return cast(CreateBuildingInspectorDTOCoolingSystemType0, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREATE_BUILDING_INSPECTOR_DTO_COOLING_SYSTEM_TYPE_0_VALUES!r}"
    )
