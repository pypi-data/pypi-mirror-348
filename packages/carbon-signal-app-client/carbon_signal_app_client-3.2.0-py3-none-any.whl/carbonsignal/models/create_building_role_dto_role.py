from typing import Literal, cast

CreateBuildingRoleDTORole = Literal["EDITOR", "VIEWER"]

CREATE_BUILDING_ROLE_DTO_ROLE_VALUES: set[CreateBuildingRoleDTORole] = {
    "EDITOR",
    "VIEWER",
}


def check_create_building_role_dto_role(value: str) -> CreateBuildingRoleDTORole:
    if value in CREATE_BUILDING_ROLE_DTO_ROLE_VALUES:
        return cast(CreateBuildingRoleDTORole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_BUILDING_ROLE_DTO_ROLE_VALUES!r}")
