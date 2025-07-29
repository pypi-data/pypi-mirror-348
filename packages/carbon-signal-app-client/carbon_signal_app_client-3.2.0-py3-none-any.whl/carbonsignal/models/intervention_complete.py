from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.emissions_savings_object import EmissionsSavingsObject
    from ..models.energy_savings_object import EnergySavingsObject
    from ..models.intervention_cost import InterventionCost
    from ..models.savings_statistic import SavingsStatistic


T = TypeVar("T", bound="InterventionComplete")


@_attrs_define
class InterventionComplete:
    """InterventionComplete.

    Attributes:
        name (str):
        description (str):
        cost (InterventionCost): InterventionCost.
        year (Union[None, int]):
        intervention_id (Union[None, int]):
        energy_savings (EnergySavingsObject): EnergySavingsObject.

            Contains energy savings for different utilities.
        energy_savings_percentage (SavingsStatistic):
        emissions_savings (EmissionsSavingsObject): EmissionsSavingsObject.

            Contains emissions savings for different utilities.
        emissions_savings_percentage (SavingsStatistic):
        status (Literal['COMPLETED']):
    """

    name: str
    description: str
    cost: "InterventionCost"
    year: None | int
    intervention_id: None | int
    energy_savings: "EnergySavingsObject"
    energy_savings_percentage: "SavingsStatistic"
    emissions_savings: "EmissionsSavingsObject"
    emissions_savings_percentage: "SavingsStatistic"
    status: Literal["COMPLETED"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        cost = self.cost.to_dict()

        year: None | int
        year = self.year

        intervention_id: None | int
        intervention_id = self.intervention_id

        energy_savings = self.energy_savings.to_dict()

        energy_savings_percentage = self.energy_savings_percentage.to_dict()

        emissions_savings = self.emissions_savings.to_dict()

        emissions_savings_percentage = self.emissions_savings_percentage.to_dict()

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "description": description,
            "cost": cost,
            "year": year,
            "intervention_id": intervention_id,
            "energy_savings": energy_savings,
            "energy_savings_percentage": energy_savings_percentage,
            "emissions_savings": emissions_savings,
            "emissions_savings_percentage": emissions_savings_percentage,
            "status": status,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.emissions_savings_object import EmissionsSavingsObject
        from ..models.energy_savings_object import EnergySavingsObject
        from ..models.intervention_cost import InterventionCost
        from ..models.savings_statistic import SavingsStatistic

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        cost = InterventionCost.from_dict(d.pop("cost"))

        def _parse_year(data: object) -> None | int:
            if data is None:
                return data
            return cast(None | int, data)

        year = _parse_year(d.pop("year"))

        def _parse_intervention_id(data: object) -> None | int:
            if data is None:
                return data
            return cast(None | int, data)

        intervention_id = _parse_intervention_id(d.pop("intervention_id"))

        energy_savings = EnergySavingsObject.from_dict(d.pop("energy_savings"))

        energy_savings_percentage = SavingsStatistic.from_dict(d.pop("energy_savings_percentage"))

        emissions_savings = EmissionsSavingsObject.from_dict(d.pop("emissions_savings"))

        emissions_savings_percentage = SavingsStatistic.from_dict(d.pop("emissions_savings_percentage"))

        status = cast(Literal["COMPLETED"], d.pop("status"))
        if status != "COMPLETED":
            raise ValueError(f"status must match const 'COMPLETED', got '{status}'")

        intervention_complete = cls(
            name=name,
            description=description,
            cost=cost,
            year=year,
            intervention_id=intervention_id,
            energy_savings=energy_savings,
            energy_savings_percentage=energy_savings_percentage,
            emissions_savings=emissions_savings,
            emissions_savings_percentage=emissions_savings_percentage,
            status=status,
        )

        intervention_complete.additional_properties = d
        return intervention_complete

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
