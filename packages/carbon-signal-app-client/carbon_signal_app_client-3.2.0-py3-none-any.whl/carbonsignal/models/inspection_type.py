from typing import Literal, cast

InspectionType = Literal["duplicate", "error", "warning"]

INSPECTION_TYPE_VALUES: set[InspectionType] = {
    "duplicate",
    "error",
    "warning",
}


def check_inspection_type(value: str) -> InspectionType:
    if value in INSPECTION_TYPE_VALUES:
        return cast(InspectionType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INSPECTION_TYPE_VALUES!r}")
