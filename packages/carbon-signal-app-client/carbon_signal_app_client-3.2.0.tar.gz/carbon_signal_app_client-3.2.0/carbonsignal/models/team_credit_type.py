from typing import Literal, cast

TeamCreditType = Literal["CALIBRATE", "PREDICT", "SIMULATE"]

TEAM_CREDIT_TYPE_VALUES: set[TeamCreditType] = {
    "CALIBRATE",
    "PREDICT",
    "SIMULATE",
}


def check_team_credit_type(value: str) -> TeamCreditType:
    if value in TEAM_CREDIT_TYPE_VALUES:
        return cast(TeamCreditType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TEAM_CREDIT_TYPE_VALUES!r}")
