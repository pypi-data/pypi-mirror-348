from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.intervention_complete import InterventionComplete
    from ..models.intervention_not_complete import InterventionNotComplete


T = TypeVar("T", bound="InterventionAnalysis")


@_attrs_define
class InterventionAnalysis:
    """InterventionAnalysis.

    This model is used to store the results of interventions/strategies applied to a baseline model.

        Attributes:
            airflow_controls (Union['InterventionComplete', 'InterventionNotComplete']):
            airside_system (Union['InterventionComplete', 'InterventionNotComplete']):
            all_electric_plant (Union['InterventionComplete', 'InterventionNotComplete']):
            equipment_controls (Union['InterventionComplete', 'InterventionNotComplete']):
            lighting_system (Union['InterventionComplete', 'InterventionNotComplete']):
            opaque_envelopes (Union['InterventionComplete', 'InterventionNotComplete']):
            ventilation_system (Union['InterventionComplete', 'InterventionNotComplete']):
            fenestration (Union['InterventionComplete', 'InterventionNotComplete']):
            all_strategies (Union['InterventionComplete', 'InterventionNotComplete']):
    """

    airflow_controls: Union["InterventionComplete", "InterventionNotComplete"]
    airside_system: Union["InterventionComplete", "InterventionNotComplete"]
    all_electric_plant: Union["InterventionComplete", "InterventionNotComplete"]
    equipment_controls: Union["InterventionComplete", "InterventionNotComplete"]
    lighting_system: Union["InterventionComplete", "InterventionNotComplete"]
    opaque_envelopes: Union["InterventionComplete", "InterventionNotComplete"]
    ventilation_system: Union["InterventionComplete", "InterventionNotComplete"]
    fenestration: Union["InterventionComplete", "InterventionNotComplete"]
    all_strategies: Union["InterventionComplete", "InterventionNotComplete"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.intervention_not_complete import InterventionNotComplete

        airflow_controls: dict[str, Any]
        if isinstance(self.airflow_controls, InterventionNotComplete):
            airflow_controls = self.airflow_controls.to_dict()
        else:
            airflow_controls = self.airflow_controls.to_dict()

        airside_system: dict[str, Any]
        if isinstance(self.airside_system, InterventionNotComplete):
            airside_system = self.airside_system.to_dict()
        else:
            airside_system = self.airside_system.to_dict()

        all_electric_plant: dict[str, Any]
        if isinstance(self.all_electric_plant, InterventionNotComplete):
            all_electric_plant = self.all_electric_plant.to_dict()
        else:
            all_electric_plant = self.all_electric_plant.to_dict()

        equipment_controls: dict[str, Any]
        if isinstance(self.equipment_controls, InterventionNotComplete):
            equipment_controls = self.equipment_controls.to_dict()
        else:
            equipment_controls = self.equipment_controls.to_dict()

        lighting_system: dict[str, Any]
        if isinstance(self.lighting_system, InterventionNotComplete):
            lighting_system = self.lighting_system.to_dict()
        else:
            lighting_system = self.lighting_system.to_dict()

        opaque_envelopes: dict[str, Any]
        if isinstance(self.opaque_envelopes, InterventionNotComplete):
            opaque_envelopes = self.opaque_envelopes.to_dict()
        else:
            opaque_envelopes = self.opaque_envelopes.to_dict()

        ventilation_system: dict[str, Any]
        if isinstance(self.ventilation_system, InterventionNotComplete):
            ventilation_system = self.ventilation_system.to_dict()
        else:
            ventilation_system = self.ventilation_system.to_dict()

        fenestration: dict[str, Any]
        if isinstance(self.fenestration, InterventionNotComplete):
            fenestration = self.fenestration.to_dict()
        else:
            fenestration = self.fenestration.to_dict()

        all_strategies: dict[str, Any]
        if isinstance(self.all_strategies, InterventionNotComplete):
            all_strategies = self.all_strategies.to_dict()
        else:
            all_strategies = self.all_strategies.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "airflow_controls": airflow_controls,
            "airside_system": airside_system,
            "all_electric_plant": all_electric_plant,
            "equipment_controls": equipment_controls,
            "lighting_system": lighting_system,
            "opaque_envelopes": opaque_envelopes,
            "ventilation_system": ventilation_system,
            "fenestration": fenestration,
            "all_strategies": all_strategies,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.intervention_complete import InterventionComplete
        from ..models.intervention_not_complete import InterventionNotComplete

        d = dict(src_dict)

        def _parse_airflow_controls(data: object) -> Union["InterventionComplete", "InterventionNotComplete"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                airflow_controls_type_0 = InterventionNotComplete.from_dict(data)

                return airflow_controls_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            airflow_controls_type_1 = InterventionComplete.from_dict(data)

            return airflow_controls_type_1

        airflow_controls = _parse_airflow_controls(d.pop("airflow_controls"))

        def _parse_airside_system(data: object) -> Union["InterventionComplete", "InterventionNotComplete"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                airside_system_type_0 = InterventionNotComplete.from_dict(data)

                return airside_system_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            airside_system_type_1 = InterventionComplete.from_dict(data)

            return airside_system_type_1

        airside_system = _parse_airside_system(d.pop("airside_system"))

        def _parse_all_electric_plant(data: object) -> Union["InterventionComplete", "InterventionNotComplete"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                all_electric_plant_type_0 = InterventionNotComplete.from_dict(data)

                return all_electric_plant_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            all_electric_plant_type_1 = InterventionComplete.from_dict(data)

            return all_electric_plant_type_1

        all_electric_plant = _parse_all_electric_plant(d.pop("all_electric_plant"))

        def _parse_equipment_controls(data: object) -> Union["InterventionComplete", "InterventionNotComplete"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                equipment_controls_type_0 = InterventionNotComplete.from_dict(data)

                return equipment_controls_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            equipment_controls_type_1 = InterventionComplete.from_dict(data)

            return equipment_controls_type_1

        equipment_controls = _parse_equipment_controls(d.pop("equipment_controls"))

        def _parse_lighting_system(data: object) -> Union["InterventionComplete", "InterventionNotComplete"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                lighting_system_type_0 = InterventionNotComplete.from_dict(data)

                return lighting_system_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            lighting_system_type_1 = InterventionComplete.from_dict(data)

            return lighting_system_type_1

        lighting_system = _parse_lighting_system(d.pop("lighting_system"))

        def _parse_opaque_envelopes(data: object) -> Union["InterventionComplete", "InterventionNotComplete"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                opaque_envelopes_type_0 = InterventionNotComplete.from_dict(data)

                return opaque_envelopes_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            opaque_envelopes_type_1 = InterventionComplete.from_dict(data)

            return opaque_envelopes_type_1

        opaque_envelopes = _parse_opaque_envelopes(d.pop("opaque_envelopes"))

        def _parse_ventilation_system(data: object) -> Union["InterventionComplete", "InterventionNotComplete"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ventilation_system_type_0 = InterventionNotComplete.from_dict(data)

                return ventilation_system_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            ventilation_system_type_1 = InterventionComplete.from_dict(data)

            return ventilation_system_type_1

        ventilation_system = _parse_ventilation_system(d.pop("ventilation_system"))

        def _parse_fenestration(data: object) -> Union["InterventionComplete", "InterventionNotComplete"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                fenestration_type_0 = InterventionNotComplete.from_dict(data)

                return fenestration_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            fenestration_type_1 = InterventionComplete.from_dict(data)

            return fenestration_type_1

        fenestration = _parse_fenestration(d.pop("fenestration"))

        def _parse_all_strategies(data: object) -> Union["InterventionComplete", "InterventionNotComplete"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                all_strategies_type_0 = InterventionNotComplete.from_dict(data)

                return all_strategies_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            all_strategies_type_1 = InterventionComplete.from_dict(data)

            return all_strategies_type_1

        all_strategies = _parse_all_strategies(d.pop("all_strategies"))

        intervention_analysis = cls(
            airflow_controls=airflow_controls,
            airside_system=airside_system,
            all_electric_plant=all_electric_plant,
            equipment_controls=equipment_controls,
            lighting_system=lighting_system,
            opaque_envelopes=opaque_envelopes,
            ventilation_system=ventilation_system,
            fenestration=fenestration,
            all_strategies=all_strategies,
        )

        intervention_analysis.additional_properties = d
        return intervention_analysis

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
