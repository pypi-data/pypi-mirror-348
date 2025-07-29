from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EnergyUseIntensities")


@_attrs_define
class EnergyUseIntensities:
    """EnergyUseIntensities.

    Attributes:
        electricity (float): Energy use intensity for the given utility.

            **Unit:** kBTU/ft2
        gas (float): Energy use intensity for the given utility.

            **Unit:** kBTU/ft2
        steam (float): Energy use intensity for the given utility.

            **Unit:** kBTU/ft2
        chilled_water (float): Energy use intensity for the given utility.

            **Unit:** kBTU/ft2
    """

    electricity: float
    gas: float
    steam: float
    chilled_water: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        electricity = self.electricity

        gas = self.gas

        steam = self.steam

        chilled_water = self.chilled_water

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
        d = dict(src_dict)
        electricity = d.pop("electricity")

        gas = d.pop("gas")

        steam = d.pop("steam")

        chilled_water = d.pop("chilled_water")

        energy_use_intensities = cls(
            electricity=electricity,
            gas=gas,
            steam=steam,
            chilled_water=chilled_water,
        )

        energy_use_intensities.additional_properties = d
        return energy_use_intensities

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
