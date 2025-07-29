from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.energy_end_use_statistic import EnergyEndUseStatistic


T = TypeVar("T", bound="EnergyEndUse")


@_attrs_define
class EnergyEndUse:
    """Energy end use model.

    Attributes:
        cooling (EnergyEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `kbtu/ft2`.
        pumps_and_fans (EnergyEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `kbtu/ft2`.
        heating (EnergyEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `kbtu/ft2`.
        lighting (EnergyEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `kbtu/ft2`.
        equipment (EnergyEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `kbtu/ft2`.
        other (EnergyEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `kbtu/ft2`.
        process (EnergyEndUseStatistic): EnergyEndUseStatistic.

            The range of estimates for a specific end use, based on Carbon Signal's baseline model in `kbtu/ft2`.
    """

    cooling: "EnergyEndUseStatistic"
    pumps_and_fans: "EnergyEndUseStatistic"
    heating: "EnergyEndUseStatistic"
    lighting: "EnergyEndUseStatistic"
    equipment: "EnergyEndUseStatistic"
    other: "EnergyEndUseStatistic"
    process: "EnergyEndUseStatistic"
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
        from ..models.energy_end_use_statistic import EnergyEndUseStatistic

        d = dict(src_dict)
        cooling = EnergyEndUseStatistic.from_dict(d.pop("cooling"))

        pumps_and_fans = EnergyEndUseStatistic.from_dict(d.pop("pumps_and_fans"))

        heating = EnergyEndUseStatistic.from_dict(d.pop("heating"))

        lighting = EnergyEndUseStatistic.from_dict(d.pop("lighting"))

        equipment = EnergyEndUseStatistic.from_dict(d.pop("equipment"))

        other = EnergyEndUseStatistic.from_dict(d.pop("other"))

        process = EnergyEndUseStatistic.from_dict(d.pop("process"))

        energy_end_use = cls(
            cooling=cooling,
            pumps_and_fans=pumps_and_fans,
            heating=heating,
            lighting=lighting,
            equipment=equipment,
            other=other,
            process=process,
        )

        energy_end_use.additional_properties = d
        return energy_end_use

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
