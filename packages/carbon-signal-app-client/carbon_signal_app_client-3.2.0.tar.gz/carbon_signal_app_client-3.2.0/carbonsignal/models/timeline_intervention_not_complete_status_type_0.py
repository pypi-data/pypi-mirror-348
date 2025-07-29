from typing import Literal, cast

TimelineInterventionNotCompleteStatusType0 = Literal["FAILED", "PROCESSING", "QUEUED"]

TIMELINE_INTERVENTION_NOT_COMPLETE_STATUS_TYPE_0_VALUES: set[TimelineInterventionNotCompleteStatusType0] = {
    "FAILED",
    "PROCESSING",
    "QUEUED",
}


def check_timeline_intervention_not_complete_status_type_0(value: str) -> TimelineInterventionNotCompleteStatusType0:
    if value in TIMELINE_INTERVENTION_NOT_COMPLETE_STATUS_TYPE_0_VALUES:
        return cast(TimelineInterventionNotCompleteStatusType0, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TIMELINE_INTERVENTION_NOT_COMPLETE_STATUS_TYPE_0_VALUES!r}"
    )
