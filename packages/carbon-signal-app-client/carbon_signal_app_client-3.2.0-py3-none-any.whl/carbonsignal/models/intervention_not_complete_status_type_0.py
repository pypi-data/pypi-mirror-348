from typing import Literal, cast

InterventionNotCompleteStatusType0 = Literal["FAILED", "PROCESSING", "QUEUED"]

INTERVENTION_NOT_COMPLETE_STATUS_TYPE_0_VALUES: set[InterventionNotCompleteStatusType0] = {
    "FAILED",
    "PROCESSING",
    "QUEUED",
}


def check_intervention_not_complete_status_type_0(value: str) -> InterventionNotCompleteStatusType0:
    if value in INTERVENTION_NOT_COMPLETE_STATUS_TYPE_0_VALUES:
        return cast(InterventionNotCompleteStatusType0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INTERVENTION_NOT_COMPLETE_STATUS_TYPE_0_VALUES!r}")
