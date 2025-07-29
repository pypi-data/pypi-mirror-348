from typing import Literal, cast

UpdateBuildingRoleDTORole = Literal["EDITOR", "VIEWER"]

UPDATE_BUILDING_ROLE_DTO_ROLE_VALUES: set[UpdateBuildingRoleDTORole] = {
    "EDITOR",
    "VIEWER",
}


def check_update_building_role_dto_role(value: str) -> UpdateBuildingRoleDTORole:
    if value in UPDATE_BUILDING_ROLE_DTO_ROLE_VALUES:
        return cast(UpdateBuildingRoleDTORole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPDATE_BUILDING_ROLE_DTO_ROLE_VALUES!r}")
