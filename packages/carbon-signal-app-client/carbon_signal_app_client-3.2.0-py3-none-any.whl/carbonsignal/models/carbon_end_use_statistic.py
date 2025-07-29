from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CarbonEndUseStatistic")


@_attrs_define
class CarbonEndUseStatistic:
    """EnergyEndUseStatistic.

    The range of estimates for a specific end use, based on Carbon Signal's baseline model in `lbsCO2e/ft2`.

        Attributes:
            estimate (float): **Unit:** lbsCO2e/ft2
            lower (float): **Unit:** lbsCO2e/ft2
            upper (float): **Unit:** lbsCO2e/ft2
    """

    estimate: float
    lower: float
    upper: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        estimate = self.estimate

        lower = self.lower

        upper = self.upper

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "estimate": estimate,
            "lower": lower,
            "upper": upper,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        estimate = d.pop("estimate")

        lower = d.pop("lower")

        upper = d.pop("upper")

        carbon_end_use_statistic = cls(
            estimate=estimate,
            lower=lower,
            upper=upper,
        )

        carbon_end_use_statistic.additional_properties = d
        return carbon_end_use_statistic

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
