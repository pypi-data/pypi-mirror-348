from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.carbon_end_use_statistic import CarbonEndUseStatistic


T = TypeVar("T", bound="CarbonEndUse")


@_attrs_define
class CarbonEndUse:
    """Carbon end use model.

    Attributes:
        cooling (CarbonEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `lbsCO2e/ft2`.
        pumps_and_fans (CarbonEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `lbsCO2e/ft2`.
        heating (CarbonEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `lbsCO2e/ft2`.
        lighting (CarbonEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `lbsCO2e/ft2`.
        equipment (CarbonEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `lbsCO2e/ft2`.
        other (CarbonEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `lbsCO2e/ft2`.
        process (CarbonEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `lbsCO2e/ft2`.
    """

    cooling: "CarbonEndUseStatistic"
    pumps_and_fans: "CarbonEndUseStatistic"
    heating: "CarbonEndUseStatistic"
    lighting: "CarbonEndUseStatistic"
    equipment: "CarbonEndUseStatistic"
    other: "CarbonEndUseStatistic"
    process: "CarbonEndUseStatistic"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cooling = self.cooling.to_dict()

        pumps_and_fans = self.pumps_and_fans.to_dict()

        heating = self.heating.to_dict()

        lighting = self.lighting.to_dict()

        equipment = self.equipment.to_dict()

        other = self.other.to_dict()

        process = self.process.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cooling": cooling,
            "pumps_and_fans": pumps_and_fans,
            "heating": heating,
            "lighting": lighting,
            "equipment": equipment,
            "other": other,
            "process": process,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.carbon_end_use_statistic import CarbonEndUseStatistic

        d = dict(src_dict)
        cooling = CarbonEndUseStatistic.from_dict(d.pop("cooling"))

        pumps_and_fans = CarbonEndUseStatistic.from_dict(d.pop("pumps_and_fans"))

        heating = CarbonEndUseStatistic.from_dict(d.pop("heating"))

        lighting = CarbonEndUseStatistic.from_dict(d.pop("lighting"))

        equipment = CarbonEndUseStatistic.from_dict(d.pop("equipment"))

        other = CarbonEndUseStatistic.from_dict(d.pop("other"))

        process = CarbonEndUseStatistic.from_dict(d.pop("process"))

        carbon_end_use = cls(
            cooling=cooling,
            pumps_and_fans=pumps_and_fans,
            heating=heating,
            lighting=lighting,
            equipment=equipment,
            other=other,
            process=process,
        )

        carbon_end_use.additional_properties = d
        return carbon_end_use

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
