from typing import Literal, cast

UpdateTeamRoleDTORole = Literal["ADMIN", "MANAGER", "OWNER", "VIEWER"]

UPDATE_TEAM_ROLE_DTO_ROLE_VALUES: set[UpdateTeamRoleDTORole] = {
    "ADMIN",
    "MANAGER",
    "OWNER",
    "VIEWER",
}


def check_update_team_role_dto_role(value: str) -> UpdateTeamRoleDTORole:
    if value in UPDATE_TEAM_ROLE_DTO_ROLE_VALUES:
        return cast(UpdateTeamRoleDTORole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPDATE_TEAM_ROLE_DTO_ROLE_VALUES!r}")
