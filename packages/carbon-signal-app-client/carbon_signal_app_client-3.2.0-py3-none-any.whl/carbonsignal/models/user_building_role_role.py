from typing import Literal, cast

UserBuildingRoleRole = Literal["EDITOR", "VIEWER"]

USER_BUILDING_ROLE_ROLE_VALUES: set[UserBuildingRoleRole] = {
    "EDITOR",
    "VIEWER",
}


def check_user_building_role_role(value: str) -> UserBuildingRoleRole:
    if value in USER_BUILDING_ROLE_ROLE_VALUES:
        return cast(UserBuildingRoleRole, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {USER_BUILDING_ROLE_ROLE_VALUES!r}")
