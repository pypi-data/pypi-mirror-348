from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UtilityMeters")


@_attrs_define
class UtilityMeters:
    """UtilityMeters.

    Attributes:
        electricity (list[float]): Electricity usage by month.

             **Unit:** kBTU
        gas (list[float]): Gas usage by month.

             **Unit:** kBTU.
        steam (list[float]): Steam usage by month.

             **Unit:** kBTU
        chilled_water (list[float]): Chilled water usage by month.

             **Unit:** kBTU
    """

    electricity: list[float]
    gas: list[float]
    steam: list[float]
    chilled_water: list[float]
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
        electricity = cast(list[float], d.pop("electricity"))

        gas = cast(list[float], d.pop("gas"))

        steam = cast(list[float], d.pop("steam"))

        chilled_water = cast(list[float], d.pop("chilled_water"))

        utility_meters = cls(
            electricity=electricity,
            gas=gas,
            steam=steam,
            chilled_water=chilled_water,
        )

        utility_meters.additional_properties = d
        return utility_meters

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
