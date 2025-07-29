from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.baseline_characterization_running import BaselineCharacterizationRunning
    from ..models.baseline_complete import BaselineComplete
    from ..models.baseline_energy_running import BaselineEnergyRunning
    from ..models.baseline_not_started import BaselineNotStarted
    from ..models.intervention_analysis import InterventionAnalysis


T = TypeVar("T", bound="BuildingResult")


@_attrs_define
class BuildingResult:
    """BuildingResult.

    Attributes:
        building_id (int):
        baseline (Union['BaselineCharacterizationRunning', 'BaselineComplete', 'BaselineEnergyRunning',
            'BaselineNotStarted', None]):
        interventions (InterventionAnalysis): InterventionAnalysis.

            This model is used to store the results of interventions/strategies applied to a baseline model.
    """

    building_id: int
    baseline: Union[
        "BaselineCharacterizationRunning", "BaselineComplete", "BaselineEnergyRunning", "BaselineNotStarted", None
    ]
    interventions: "InterventionAnalysis"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.baseline_characterization_running import BaselineCharacterizationRunning
        from ..models.baseline_complete import BaselineComplete
        from ..models.baseline_energy_running import BaselineEnergyRunning
        from ..models.baseline_not_started import BaselineNotStarted

        building_id = self.building_id

        baseline: None | dict[str, Any]
        if isinstance(
            self.baseline,
            BaselineNotStarted | BaselineCharacterizationRunning | BaselineEnergyRunning | BaselineComplete,
        ):
            baseline = self.baseline.to_dict()
        else:
            baseline = self.baseline

        interventions = self.interventions.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "building_id": building_id,
            "baseline": baseline,
            "interventions": interventions,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.baseline_characterization_running import BaselineCharacterizationRunning
        from ..models.baseline_complete import BaselineComplete
        from ..models.baseline_energy_running import BaselineEnergyRunning
        from ..models.baseline_not_started import BaselineNotStarted
        from ..models.intervention_analysis import InterventionAnalysis

        d = dict(src_dict)
        building_id = d.pop("building_id")

        def _parse_baseline(
            data: object,
        ) -> Union[
            "BaselineCharacterizationRunning", "BaselineComplete", "BaselineEnergyRunning", "BaselineNotStarted", None
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                baseline_type_0 = BaselineNotStarted.from_dict(data)

                return baseline_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                baseline_type_1 = BaselineCharacterizationRunning.from_dict(data)

                return baseline_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                baseline_type_2 = BaselineEnergyRunning.from_dict(data)

                return baseline_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                baseline_type_3 = BaselineComplete.from_dict(data)

                return baseline_type_3
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "BaselineCharacterizationRunning",
                    "BaselineComplete",
                    "BaselineEnergyRunning",
                    "BaselineNotStarted",
                    None,
                ],
                data,
            )

        baseline = _parse_baseline(d.pop("baseline"))

        interventions = InterventionAnalysis.from_dict(d.pop("interventions"))

        building_result = cls(
            building_id=building_id,
            baseline=baseline,
            interventions=interventions,
        )

        building_result.additional_properties = d
        return building_result

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
