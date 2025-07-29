from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.emission_factor import EmissionFactor


T = TypeVar("T", bound="EmissionFactors")


@_attrs_define
class EmissionFactors:
    """EmissionFactors.

    Attributes:
        electricity (EmissionFactor): EmissionFactor. All units of lbs/kBtu.
        gas (EmissionFactor): EmissionFactor. All units of lbs/kBtu.
        steam (EmissionFactor): EmissionFactor. All units of lbs/kBtu.
        chilled_water (EmissionFactor): EmissionFactor. All units of lbs/kBtu.
    """

    electricity: "EmissionFactor"
    gas: "EmissionFactor"
    steam: "EmissionFactor"
    chilled_water: "EmissionFactor"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        electricity = self.electricity.to_dict()

        gas = self.gas.to_dict()

        steam = self.steam.to_dict()

        chilled_water = self.chilled_water.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "electricity": electricity,
            "gas": gas,
            "steam": steam,
            "chilled_water": chilled_water,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.emission_factor import EmissionFactor

        d = dict(src_dict)
        electricity = EmissionFactor.from_dict(d.pop("electricity"))

        gas = EmissionFactor.from_dict(d.pop("gas"))

        steam = EmissionFactor.from_dict(d.pop("steam"))

        chilled_water = EmissionFactor.from_dict(d.pop("chilled_water"))

        emission_factors = cls(
            electricity=electricity,
            gas=gas,
            steam=steam,
            chilled_water=chilled_water,
        )

        emission_factors.additional_properties = d
        return emission_factors

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
