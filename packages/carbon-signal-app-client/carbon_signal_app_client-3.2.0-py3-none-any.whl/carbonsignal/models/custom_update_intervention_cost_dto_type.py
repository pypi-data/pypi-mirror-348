from typing import Literal, cast

CustomUpdateInterventionCostDTOType = Literal["NORMALIZED", "TOTAL"]

CUSTOM_UPDATE_INTERVENTION_COST_DTO_TYPE_VALUES: set[CustomUpdateInterventionCostDTOType] = {
    "NORMALIZED",
    "TOTAL",
}


def check_custom_update_intervention_cost_dto_type(value: str) -> CustomUpdateInterventionCostDTOType:
    if value in CUSTOM_UPDATE_INTERVENTION_COST_DTO_TYPE_VALUES:
        return cast(CustomUpdateInterventionCostDTOType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {CUSTOM_UPDATE_INTERVENTION_COST_DTO_TYPE_VALUES!r}")
