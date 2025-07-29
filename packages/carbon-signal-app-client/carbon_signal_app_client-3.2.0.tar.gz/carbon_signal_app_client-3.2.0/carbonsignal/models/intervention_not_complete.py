from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.intervention_not_complete_status_type_0 import (
    InterventionNotCompleteStatusType0,
    check_intervention_not_complete_status_type_0,
)

if TYPE_CHECKING:
    from ..models.intervention_cost import InterventionCost


T = TypeVar("T", bound="InterventionNotComplete")


@_attrs_define
class InterventionNotComplete:
    """InterventionNotComplete.

    Attributes:
        name (str):
        description (str):
        cost (InterventionCost): InterventionCost.
        year (Union[None, int]):
        intervention_id (Union[None, int]):
        emissions_savings (None):
        emissions_savings_percentage (None):
        energy_savings (None):
        energy_savings_percentage (None):
        status (Union[InterventionNotCompleteStatusType0, None]): Status of the intervention.

            **Allowed values:**

            - `PROCESSING`
            - `QUEUED`
            - `FAILED`
            - `null` *(represents that the intervention has not started and is likely waiting to be queued)*
    """

    name: str
    description: str
    cost: "InterventionCost"
    year: None | int
    intervention_id: None | int
    emissions_savings: None
    emissions_savings_percentage: None
    energy_savings: None
    energy_savings_percentage: None
    status: InterventionNotCompleteStatusType0 | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        cost = self.cost.to_dict()

        year: None | int
        year = self.year

        intervention_id: None | int
        intervention_id = self.intervention_id

        emissions_savings = self.emissions_savings

        emissions_savings_percentage = self.emissions_savings_percentage

        energy_savings = self.energy_savings

        energy_savings_percentage = self.energy_savings_percentage

        status: None | str
        status = self.status if isinstance(self.status, str) else self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "description": description,
            "cost": cost,
            "year": year,
            "intervention_id": intervention_id,
            "emissions_savings": emissions_savings,
            "emissions_savings_percentage": emissions_savings_percentage,
            "energy_savings": energy_savings,
            "energy_savings_percentage": energy_savings_percentage,
            "status": status,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.intervention_cost import InterventionCost

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

        emissions_savings = d.pop("emissions_savings")

        emissions_savings_percentage = d.pop("emissions_savings_percentage")

        energy_savings = d.pop("energy_savings")

        energy_savings_percentage = d.pop("energy_savings_percentage")

        def _parse_status(data: object) -> InterventionNotCompleteStatusType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = check_intervention_not_complete_status_type_0(data)

                return status_type_0
            except:  # noqa: E722
                pass
            return cast(InterventionNotCompleteStatusType0 | None, data)

        status = _parse_status(d.pop("status"))

        intervention_not_complete = cls(
            name=name,
            description=description,
            cost=cost,
            year=year,
            intervention_id=intervention_id,
            emissions_savings=emissions_savings,
            emissions_savings_percentage=emissions_savings_percentage,
            energy_savings=energy_savings,
            energy_savings_percentage=energy_savings_percentage,
            status=status,
        )

        intervention_not_complete.additional_properties = d
        return intervention_not_complete

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
