from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.custom_update_intervention_cost_dto_type import (
    CustomUpdateInterventionCostDTOType,
    check_custom_update_intervention_cost_dto_type,
)

T = TypeVar("T", bound="CustomUpdateInterventionCostDTO")


@_attrs_define
class CustomUpdateInterventionCostDTO:
    """CustomUpdateInterventionCostDTO.

    Attributes:
        cost (float): Cost of the intervention.
        type_ (CustomUpdateInterventionCostDTOType):
        source (Literal['CUSTOM']):
    """

    cost: float
    type_: CustomUpdateInterventionCostDTOType
    source: Literal["CUSTOM"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cost = self.cost

        type_: str = self.type_

        source = self.source

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

        type_ = check_custom_update_intervention_cost_dto_type(d.pop("type"))

        source = cast(Literal["CUSTOM"], d.pop("source"))
        if source != "CUSTOM":
            raise ValueError(f"source must match const 'CUSTOM', got '{source}'")

        custom_update_intervention_cost_dto = cls(
            cost=cost,
            type_=type_,
            source=source,
        )

        custom_update_intervention_cost_dto.additional_properties = d
        return custom_update_intervention_cost_dto

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
