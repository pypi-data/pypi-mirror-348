from typing import Literal, cast

UpdateUserSettingsDTODisplayUnit = Literal["IMPERIAL", "METRIC"]

UPDATE_USER_SETTINGS_DTO_DISPLAY_UNIT_VALUES: set[UpdateUserSettingsDTODisplayUnit] = {
    "IMPERIAL",
    "METRIC",
}


def check_update_user_settings_dto_display_unit(value: str) -> UpdateUserSettingsDTODisplayUnit:
    if value in UPDATE_USER_SETTINGS_DTO_DISPLAY_UNIT_VALUES:
        return cast(UpdateUserSettingsDTODisplayUnit, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPDATE_USER_SETTINGS_DTO_DISPLAY_UNIT_VALUES!r}")
