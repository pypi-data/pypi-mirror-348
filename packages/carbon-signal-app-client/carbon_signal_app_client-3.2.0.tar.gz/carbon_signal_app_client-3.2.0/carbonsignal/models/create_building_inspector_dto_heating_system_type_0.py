from typing import Literal, cast

CreateBuildingInspectorDTOHeatingSystemType0 = Literal["DISTRICT", "ELECTRICITY", "GAS", "NO_SYSTEM"]

CREATE_BUILDING_INSPECTOR_DTO_HEATING_SYSTEM_TYPE_0_VALUES: set[CreateBuildingInspectorDTOHeatingSystemType0] = {
    "DISTRICT",
    "ELECTRICITY",
    "GAS",
    "NO_SYSTEM",
}


def check_create_building_inspector_dto_heating_system_type_0(
    value: str,
) -> CreateBuildingInspectorDTOHeatingSystemType0:
    if value in CREATE_BUILDING_INSPECTOR_DTO_HEATING_SYSTEM_TYPE_0_VALUES:
        return cast(CreateBuildingInspectorDTOHeatingSystemType0, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREATE_BUILDING_INSPECTOR_DTO_HEATING_SYSTEM_TYPE_0_VALUES!r}"
    )
