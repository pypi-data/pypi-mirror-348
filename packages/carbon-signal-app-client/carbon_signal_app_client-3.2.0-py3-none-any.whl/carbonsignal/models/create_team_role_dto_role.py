from typing import Literal, cast

CreateTeamRoleDTORole = Literal["ADMIN", "MANAGER", "OWNER", "VIEWER"]

CREATE_TEAM_ROLE_DTO_ROLE_VALUES: set[CreateTeamRoleDTORole] = {
    "ADMIN",
    "MANAGER",
    "OWNER",
    "VIEWER",
}


def check_create_team_role_dto_role(value: str) -> CreateTeamRoleDTORole:
    if value in CREATE_TEAM_ROLE_DTO_ROLE_VALUES:
        return cast(CreateTeamRoleDTORole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CREATE_TEAM_ROLE_DTO_ROLE_VALUES!r}")
