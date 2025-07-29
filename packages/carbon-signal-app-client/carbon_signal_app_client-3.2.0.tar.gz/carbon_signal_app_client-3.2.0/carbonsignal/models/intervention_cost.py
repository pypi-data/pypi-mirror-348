from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.intervention_cost_source import InterventionCostSource, check_intervention_cost_source
from ..models.intervention_cost_type import InterventionCostType, check_intervention_cost_type

T = TypeVar("T", bound="InterventionCost")


@_attrs_define
class InterventionCost:
    """InterventionCost.

    Attributes:
        cost (float):
        type_ (InterventionCostType):
        source (InterventionCostSource): Is the intervention cost based on user input, or a Carbon Signal default?
    """

    cost: float
    type_: InterventionCostType
    source: InterventionCostSource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cost = self.cost

        type_: str = self.type_

        source: str = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cost": cost,
            "type": type_,
            "source": source,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cost = d.pop("cost")

        type_ = check_intervention_cost_type(d.pop("type"))

        source = check_intervention_cost_source(d.pop("source"))

        intervention_cost = cls(
            cost=cost,
            type_=type_,
            source=source,
        )

        intervention_cost.additional_properties = d
        return intervention_cost

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
