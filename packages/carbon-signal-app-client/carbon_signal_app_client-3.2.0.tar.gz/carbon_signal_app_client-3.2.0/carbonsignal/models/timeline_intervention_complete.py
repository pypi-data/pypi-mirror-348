from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.carbon_result_statistic import CarbonResultStatistic
    from ..models.energy_result_statistic import EnergyResultStatistic


T = TypeVar("T", bound="TimelineInterventionComplete")


@_attrs_define
class TimelineInterventionComplete:
    """Timeline InterventionComplete.

    Attributes:
        energy (EnergyResultStatistic): EnergyResultStatistic.

            The energy result statistics for a specific utility.
        emissions (CarbonResultStatistic): EnergyResultStatistic.

            The carbon statistics for a specific utility.
        status (Literal['COMPLETED']):
    """

    energy: "EnergyResultStatistic"
    emissions: "CarbonResultStatistic"
    status: Literal["COMPLETED"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        energy = self.energy.to_dict()

        emissions = self.emissions.to_dict()

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "energy": energy,
            "emissions": emissions,
            "status": status,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.carbon_result_statistic import CarbonResultStatistic
        from ..models.energy_result_statistic import EnergyResultStatistic

        d = dict(src_dict)
        energy = EnergyResultStatistic.from_dict(d.pop("energy"))

        emissions = CarbonResultStatistic.from_dict(d.pop("emissions"))

        status = cast(Literal["COMPLETED"], d.pop("status"))
        if status != "COMPLETED":
            raise ValueError(f"status must match const 'COMPLETED', got '{status}'")

        timeline_intervention_complete = cls(
            energy=energy,
            emissions=emissions,
            status=status,
        )

        timeline_intervention_complete.additional_properties = d
        return timeline_intervention_complete

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
