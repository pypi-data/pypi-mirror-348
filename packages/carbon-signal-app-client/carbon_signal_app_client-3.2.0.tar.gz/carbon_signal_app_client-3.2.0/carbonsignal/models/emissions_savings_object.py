from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.savings_statistic_lbs_co2e_per_ft_2 import SavingsStatisticLbsCO2EPerFt2


T = TypeVar("T", bound="EmissionsSavingsObject")


@_attrs_define
class EmissionsSavingsObject:
    """EmissionsSavingsObject.

    Contains emissions savings for different utilities.

        Attributes:
            electricity (SavingsStatisticLbsCO2EPerFt2):
            gas (SavingsStatisticLbsCO2EPerFt2):
            chilled_water (SavingsStatisticLbsCO2EPerFt2):
            steam (SavingsStatisticLbsCO2EPerFt2):
            total (SavingsStatisticLbsCO2EPerFt2):
    """

    electricity: "SavingsStatisticLbsCO2EPerFt2"
    gas: "SavingsStatisticLbsCO2EPerFt2"
    chilled_water: "SavingsStatisticLbsCO2EPerFt2"
    steam: "SavingsStatisticLbsCO2EPerFt2"
    total: "SavingsStatisticLbsCO2EPerFt2"
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
        from ..models.savings_statistic_lbs_co2e_per_ft_2 import SavingsStatisticLbsCO2EPerFt2

        d = dict(src_dict)
        electricity = SavingsStatisticLbsCO2EPerFt2.from_dict(d.pop("electricity"))

        gas = SavingsStatisticLbsCO2EPerFt2.from_dict(d.pop("gas"))

        chilled_water = SavingsStatisticLbsCO2EPerFt2.from_dict(d.pop("chilled_water"))

        steam = SavingsStatisticLbsCO2EPerFt2.from_dict(d.pop("steam"))

        total = SavingsStatisticLbsCO2EPerFt2.from_dict(d.pop("total"))

        emissions_savings_object = cls(
            electricity=electricity,
            gas=gas,
            chilled_water=chilled_water,
            steam=steam,
            total=total,
        )

        emissions_savings_object.additional_properties = d
        return emissions_savings_object

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
