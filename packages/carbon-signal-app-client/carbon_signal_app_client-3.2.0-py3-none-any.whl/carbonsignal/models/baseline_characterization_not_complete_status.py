from typing import Literal, cast

BaselineCharacterizationNotCompleteStatus = Literal["FAILED", "PROCESSING", "QUEUED"]

BASELINE_CHARACTERIZATION_NOT_COMPLETE_STATUS_VALUES: set[BaselineCharacterizationNotCompleteStatus] = {
    "FAILED",
    "PROCESSING",
    "QUEUED",
}


def check_baseline_characterization_not_complete_status(value: str) -> BaselineCharacterizationNotCompleteStatus:
    if value in BASELINE_CHARACTERIZATION_NOT_COMPLETE_STATUS_VALUES:
        return cast(BaselineCharacterizationNotCompleteStatus, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {BASELINE_CHARACTERIZATION_NOT_COMPLETE_STATUS_VALUES!r}"
    )
