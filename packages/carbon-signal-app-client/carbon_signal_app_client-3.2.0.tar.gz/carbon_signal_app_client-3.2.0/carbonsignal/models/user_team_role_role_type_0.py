from typing import Literal, cast

UserTeamRoleRoleType0 = Literal["ADMIN", "MANAGER", "OWNER", "VIEWER"]

USER_TEAM_ROLE_ROLE_TYPE_0_VALUES: set[UserTeamRoleRoleType0] = {
    "ADMIN",
    "MANAGER",
    "OWNER",
    "VIEWER",
}


def check_user_team_role_role_type_0(value: str) -> UserTeamRoleRoleType0:
    if value in USER_TEAM_ROLE_ROLE_TYPE_0_VALUES:
        return cast(UserTeamRoleRoleType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {USER_TEAM_ROLE_ROLE_TYPE_0_VALUES!r}")
