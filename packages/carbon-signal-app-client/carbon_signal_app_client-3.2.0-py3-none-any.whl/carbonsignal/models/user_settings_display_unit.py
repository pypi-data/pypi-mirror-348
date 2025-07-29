from typing import Literal, cast

UserSettingsDisplayUnit = Literal["IMPERIAL", "METRIC"]

USER_SETTINGS_DISPLAY_UNIT_VALUES: set[UserSettingsDisplayUnit] = {
    "IMPERIAL",
    "METRIC",
}


def check_user_settings_display_unit(value: str) -> UserSettingsDisplayUnit:
    if value in USER_SETTINGS_DISPLAY_UNIT_VALUES:
        return cast(UserSettingsDisplayUnit, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {USER_SETTINGS_DISPLAY_UNIT_VALUES!r}")
