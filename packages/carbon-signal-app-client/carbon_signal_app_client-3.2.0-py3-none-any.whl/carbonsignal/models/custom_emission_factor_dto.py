from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CustomEmissionFactorDTO")


@_attrs_define
class CustomEmissionFactorDTO:
    """CustomEmissionFactor.

    Attributes:
        value (float):
        source (Literal['CUSTOM']):
    """

    value: float
    source: Literal["CUSTOM"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        source = self.source

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

        source = cast(Literal["CUSTOM"], d.pop("source"))
        if source != "CUSTOM":
            raise ValueError(f"source must match const 'CUSTOM', got '{source}'")

        custom_emission_factor_dto = cls(
            value=value,
            source=source,
        )

        custom_emission_factor_dto.additional_properties = d
        return custom_emission_factor_dto

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
