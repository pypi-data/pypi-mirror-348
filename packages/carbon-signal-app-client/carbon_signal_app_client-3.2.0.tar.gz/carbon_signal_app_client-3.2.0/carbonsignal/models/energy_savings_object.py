from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.savings_statistic_kbtu_per_ft_2 import SavingsStatisticKbtuPerFt2


T = TypeVar("T", bound="EnergySavingsObject")


@_attrs_define
class EnergySavingsObject:
    """EnergySavingsObject.

    Contains energy savings for different utilities.

        Attributes:
            electricity (SavingsStatisticKbtuPerFt2):
            gas (SavingsStatisticKbtuPerFt2):
            chilled_water (SavingsStatisticKbtuPerFt2):
            steam (SavingsStatisticKbtuPerFt2):
            total (SavingsStatisticKbtuPerFt2):
    """

    electricity: "SavingsStatisticKbtuPerFt2"
    gas: "SavingsStatisticKbtuPerFt2"
    chilled_water: "SavingsStatisticKbtuPerFt2"
    steam: "SavingsStatisticKbtuPerFt2"
    total: "SavingsStatisticKbtuPerFt2"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        electricity = self.electricity.to_dict()

        gas = self.gas.to_dict()

        chilled_water = self.chilled_water.to_dict()

        steam = self.steam.to_dict()

        total = self.total.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "electricity": electricity,
            "gas": gas,
            "chilled_water": chilled_water,
            "steam": steam,
            "total": total,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.savings_statistic_kbtu_per_ft_2 import SavingsStatisticKbtuPerFt2

        d = dict(src_dict)
        electricity = SavingsStatisticKbtuPerFt2.from_dict(d.pop("electricity"))

        gas = SavingsStatisticKbtuPerFt2.from_dict(d.pop("gas"))

        chilled_water = SavingsStatisticKbtuPerFt2.from_dict(d.pop("chilled_water"))

        steam = SavingsStatisticKbtuPerFt2.from_dict(d.pop("steam"))

        total = SavingsStatisticKbtuPerFt2.from_dict(d.pop("total"))

        energy_savings_object = cls(
            electricity=electricity,
            gas=gas,
            chilled_water=chilled_water,
            steam=steam,
            total=total,
        )

        energy_savings_object.additional_properties = d
        return energy_savings_object

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
