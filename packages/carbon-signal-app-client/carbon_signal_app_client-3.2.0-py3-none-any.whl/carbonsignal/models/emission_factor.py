from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.emission_factor_source import EmissionFactorSource, check_emission_factor_source

T = TypeVar("T", bound="EmissionFactor")


@_attrs_define
class EmissionFactor:
    """EmissionFactor. All units of lbs/kBtu.

    Attributes:
        value (float): Emission factor for the utility.

            **Unit:** lbs/kBtu
        source (EmissionFactorSource): Is the emission factor based on user input, or a Carbon Signal default?
    """

    value: float
    source: EmissionFactorSource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        source: str = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "value": value,
            "source": source,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        value = d.pop("value")

        source = check_emission_factor_source(d.pop("source"))

        emission_factor = cls(
            value=value,
            source=source,
        )

        emission_factor.additional_properties = d
        return emission_factor

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
