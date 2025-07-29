from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AdjustedUtilityMeters")


@_attrs_define
class AdjustedUtilityMeters:
    """AdjustedUtilityMeters.

    Attributes:
        electricity (Union[None, list[float]]): Adjusted electricity usage by month, if applicable.

             **Unit:** kBTU
        gas (Union[None, list[float]]): Adjusted gas usage by month, if applicable.

             **Unit:** kBTU.
        steam (Union[None, list[float]]): Adjusted steam usage by month, if applicable.

             **Unit:** kBTU
        chilled_water (Union[None, list[float]]): Adjusted chilled water usage by month, if applicable.

             **Unit:** kBTU
    """

    electricity: None | list[float]
    gas: None | list[float]
    steam: None | list[float]
    chilled_water: None | list[float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        electricity: None | list[float]
        electricity = self.electricity if isinstance(self.electricity, list) else self.electricity

        gas: None | list[float]
        gas = self.gas if isinstance(self.gas, list) else self.gas

        steam: None | list[float]
        steam = self.steam if isinstance(self.steam, list) else self.steam

        chilled_water: None | list[float]
        chilled_water = self.chilled_water if isinstance(self.chilled_water, list) else self.chilled_water

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

        def _parse_electricity(data: object) -> None | list[float]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                electricity_type_0 = cast(list[float], data)

                return electricity_type_0
            except:  # noqa: E722
                pass
            return cast(None | list[float], data)

        electricity = _parse_electricity(d.pop("electricity"))

        def _parse_gas(data: object) -> None | list[float]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                gas_type_0 = cast(list[float], data)

                return gas_type_0
            except:  # noqa: E722
                pass
            return cast(None | list[float], data)

        gas = _parse_gas(d.pop("gas"))

        def _parse_steam(data: object) -> None | list[float]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                steam_type_0 = cast(list[float], data)

                return steam_type_0
            except:  # noqa: E722
                pass
            return cast(None | list[float], data)

        steam = _parse_steam(d.pop("steam"))

        def _parse_chilled_water(data: object) -> None | list[float]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                chilled_water_type_0 = cast(list[float], data)

                return chilled_water_type_0
            except:  # noqa: E722
                pass
            return cast(None | list[float], data)

        chilled_water = _parse_chilled_water(d.pop("chilled_water"))

        adjusted_utility_meters = cls(
            electricity=electricity,
            gas=gas,
            steam=steam,
            chilled_water=chilled_water,
        )

        adjusted_utility_meters.additional_properties = d
        return adjusted_utility_meters

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
