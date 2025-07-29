from typing import Literal, cast

InterventionCostType = Literal["NORMALIZED", "TOTAL"]

INTERVENTION_COST_TYPE_VALUES: set[InterventionCostType] = {
    "NORMALIZED",
    "TOTAL",
}


def check_intervention_cost_type(value: str) -> InterventionCostType:
    if value in INTERVENTION_COST_TYPE_VALUES:
        return cast(InterventionCostType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INTERVENTION_COST_TYPE_VALUES!r}")
