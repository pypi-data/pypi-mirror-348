from typing import Literal, cast

BuildingStatus = Literal["COMPLETED", "FAILED", "NOT_STARTED", "QUEUED", "RUNNING"]

BUILDING_STATUS_VALUES: set[BuildingStatus] = {
    "COMPLETED",
    "FAILED",
    "NOT_STARTED",
    "QUEUED",
    "RUNNING",
}


def check_building_status(value: str) -> BuildingStatus:
    if value in BUILDING_STATUS_VALUES:
        return cast(BuildingStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BUILDING_STATUS_VALUES!r}")
