from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.energy_result_statistic import EnergyResultStatistic


T = TypeVar("T", bound="BuildingEnergyResultMeters")


@_attrs_define
class BuildingEnergyResultMeters:
    """BuildingEnergyResultMeters.

    Attributes:
        electricity (list['EnergyResultStatistic']):
        gas (list['EnergyResultStatistic']):
        steam (list['EnergyResultStatistic']):
        chilled_water (list['EnergyResultStatistic']):
    """

    electricity: list["EnergyResultStatistic"]
    gas: list["EnergyResultStatistic"]
    steam: list["EnergyResultStatistic"]
    chilled_water: list["EnergyResultStatistic"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        electricity = []
        for electricity_item_data in self.electricity:
            electricity_item = electricity_item_data.to_dict()
            electricity.append(electricity_item)

        gas = []
        for gas_item_data in self.gas:
            gas_item = gas_item_data.to_dict()
            gas.append(gas_item)

        steam = []
        for steam_item_data in self.steam:
            steam_item = steam_item_data.to_dict()
            steam.append(steam_item)

        chilled_water = []
        for chilled_water_item_data in self.chilled_water:
            chilled_water_item = chilled_water_item_data.to_dict()
            chilled_water.append(chilled_water_item)

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
        from ..models.energy_result_statistic import EnergyResultStatistic

        d = dict(src_dict)
        electricity = []
        _electricity = d.pop("electricity")
        for electricity_item_data in _electricity:
            electricity_item = EnergyResultStatistic.from_dict(electricity_item_data)

            electricity.append(electricity_item)

        gas = []
        _gas = d.pop("gas")
        for gas_item_data in _gas:
            gas_item = EnergyResultStatistic.from_dict(gas_item_data)

            gas.append(gas_item)

        steam = []
        _steam = d.pop("steam")
        for steam_item_data in _steam:
            steam_item = EnergyResultStatistic.from_dict(steam_item_data)

            steam.append(steam_item)

        chilled_water = []
        _chilled_water = d.pop("chilled_water")
        for chilled_water_item_data in _chilled_water:
            chilled_water_item = EnergyResultStatistic.from_dict(chilled_water_item_data)

            chilled_water.append(chilled_water_item)

        building_energy_result_meters = cls(
            electricity=electricity,
            gas=gas,
            steam=steam,
            chilled_water=chilled_water,
        )

        building_energy_result_meters.additional_properties = d
        return building_energy_result_meters

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
