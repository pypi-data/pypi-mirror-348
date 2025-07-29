from typing import Literal, cast

InterventionCostSource = Literal["CUSTOM", "DEFAULT"]

INTERVENTION_COST_SOURCE_VALUES: set[InterventionCostSource] = {
    "CUSTOM",
    "DEFAULT",
}


def check_intervention_cost_source(value: str) -> InterventionCostSource:
    if value in INTERVENTION_COST_SOURCE_VALUES:
        return cast(InterventionCostSource, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {INTERVENTION_COST_SOURCE_VALUES!r}")
