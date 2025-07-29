from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DefaultUpdateInterventionCostDTO")


@_attrs_define
class DefaultUpdateInterventionCostDTO:
    """DefaultUpdateInterventionCostDTO.

    Attributes:
        source (Literal['DEFAULT']):
    """

    source: Literal["DEFAULT"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "source": source,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = cast(Literal["DEFAULT"], d.pop("source"))
        if source != "DEFAULT":
            raise ValueError(f"source must match const 'DEFAULT', got '{source}'")

        default_update_intervention_cost_dto = cls(
            source=source,
        )

        default_update_intervention_cost_dto.additional_properties = d
        return default_update_intervention_cost_dto

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
