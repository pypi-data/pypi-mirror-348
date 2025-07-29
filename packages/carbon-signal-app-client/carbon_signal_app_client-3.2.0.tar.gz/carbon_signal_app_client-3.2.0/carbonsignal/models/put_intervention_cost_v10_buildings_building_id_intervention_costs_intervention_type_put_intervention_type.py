from typing import Literal, cast

PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionTypePutInterventionType = Literal[
    "airflow_controls",
    "airside_system",
    "all_electric_plant",
    "equipment_controls",
    "fenestration",
    "lighting_system",
    "opaque_envelopes",
    "ventilation_system",
]

PUT_INTERVENTION_COST_V10_BUILDINGS_BUILDING_ID_INTERVENTION_COSTS_INTERVENTION_TYPE_PUT_INTERVENTION_TYPE_VALUES: set[
    PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionTypePutInterventionType
] = {
    "airflow_controls",
    "airside_system",
    "all_electric_plant",
    "equipment_controls",
    "fenestration",
    "lighting_system",
    "opaque_envelopes",
    "ventilation_system",
}


def check_put_intervention_cost_v10_buildings_building_id_intervention_costs_intervention_type_put_intervention_type(
    value: str,
) -> PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionTypePutInterventionType:
    if (
        value
        in PUT_INTERVENTION_COST_V10_BUILDINGS_BUILDING_ID_INTERVENTION_COSTS_INTERVENTION_TYPE_PUT_INTERVENTION_TYPE_VALUES
    ):
        return cast(
            PutInterventionCostV10BuildingsBuildingIdInterventionCostsInterventionTypePutInterventionType, value
        )
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PUT_INTERVENTION_COST_V10_BUILDINGS_BUILDING_ID_INTERVENTION_COSTS_INTERVENTION_TYPE_PUT_INTERVENTION_TYPE_VALUES!r}"
    )
