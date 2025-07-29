from typing import Literal, cast

BaselineEnergyNotCompleteStatus = Literal["FAILED", "PROCESSING", "QUEUED"]

BASELINE_ENERGY_NOT_COMPLETE_STATUS_VALUES: set[BaselineEnergyNotCompleteStatus] = {
    "FAILED",
    "PROCESSING",
    "QUEUED",
}


def check_baseline_energy_not_complete_status(value: str) -> BaselineEnergyNotCompleteStatus:
    if value in BASELINE_ENERGY_NOT_COMPLETE_STATUS_VALUES:
        return cast(BaselineEnergyNotCompleteStatus, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BASELINE_ENERGY_NOT_COMPLETE_STATUS_VALUES!r}")
