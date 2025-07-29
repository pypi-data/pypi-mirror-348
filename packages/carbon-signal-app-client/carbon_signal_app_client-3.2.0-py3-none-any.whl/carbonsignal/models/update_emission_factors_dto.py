from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.custom_emission_factor_dto import CustomEmissionFactorDTO
    from ..models.default_emission_factor_dto import DefaultEmissionFactorDTO


T = TypeVar("T", bound="UpdateEmissionFactorsDTO")


@_attrs_define
class UpdateEmissionFactorsDTO:
    """UpdateEmissionFactors.

    Attributes:
        electricity (Union['CustomEmissionFactorDTO', 'DefaultEmissionFactorDTO']): Emission factor, either with a
            custom value set, or an object representing Carbon Signal defaults.
        gas (Union['CustomEmissionFactorDTO', 'DefaultEmissionFactorDTO']): Emission factor, either with a custom value
            set, or an object representing Carbon Signal defaults.
        steam (Union['CustomEmissionFactorDTO', 'DefaultEmissionFactorDTO']): Emission factor, either with a custom
            value set, or an object representing Carbon Signal defaults.
        chilled_water (Union['CustomEmissionFactorDTO', 'DefaultEmissionFactorDTO']): Emission factor, either with a
            custom value set, or an object representing Carbon Signal defaults.
    """

    electricity: Union["CustomEmissionFactorDTO", "DefaultEmissionFactorDTO"]
    gas: Union["CustomEmissionFactorDTO", "DefaultEmissionFactorDTO"]
    steam: Union["CustomEmissionFactorDTO", "DefaultEmissionFactorDTO"]
    chilled_water: Union["CustomEmissionFactorDTO", "DefaultEmissionFactorDTO"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.custom_emission_factor_dto import CustomEmissionFactorDTO

        electricity: dict[str, Any]
        if isinstance(self.electricity, CustomEmissionFactorDTO):
            electricity = self.electricity.to_dict()
        else:
            electricity = self.electricity.to_dict()

        gas: dict[str, Any]
        gas = self.gas.to_dict() if isinstance(self.gas, CustomEmissionFactorDTO) else self.gas.to_dict()

        steam: dict[str, Any]
        steam = self.steam.to_dict() if isinstance(self.steam, CustomEmissionFactorDTO) else self.steam.to_dict()

        chilled_water: dict[str, Any]
        if isinstance(self.chilled_water, CustomEmissionFactorDTO):
            chilled_water = self.chilled_water.to_dict()
        else:
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
        from ..models.custom_emission_factor_dto import CustomEmissionFactorDTO
        from ..models.default_emission_factor_dto import DefaultEmissionFactorDTO

        d = dict(src_dict)

        def _parse_electricity(data: object) -> Union["CustomEmissionFactorDTO", "DefaultEmissionFactorDTO"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                electricity_type_0 = CustomEmissionFactorDTO.from_dict(data)

                return electricity_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            electricity_type_1 = DefaultEmissionFactorDTO.from_dict(data)

            return electricity_type_1

        electricity = _parse_electricity(d.pop("electricity"))

        def _parse_gas(data: object) -> Union["CustomEmissionFactorDTO", "DefaultEmissionFactorDTO"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                gas_type_0 = CustomEmissionFactorDTO.from_dict(data)

                return gas_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            gas_type_1 = DefaultEmissionFactorDTO.from_dict(data)

            return gas_type_1

        gas = _parse_gas(d.pop("gas"))

        def _parse_steam(data: object) -> Union["CustomEmissionFactorDTO", "DefaultEmissionFactorDTO"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                steam_type_0 = CustomEmissionFactorDTO.from_dict(data)

                return steam_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            steam_type_1 = DefaultEmissionFactorDTO.from_dict(data)

            return steam_type_1

        steam = _parse_steam(d.pop("steam"))

        def _parse_chilled_water(data: object) -> Union["CustomEmissionFactorDTO", "DefaultEmissionFactorDTO"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                chilled_water_type_0 = CustomEmissionFactorDTO.from_dict(data)

                return chilled_water_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            chilled_water_type_1 = DefaultEmissionFactorDTO.from_dict(data)

            return chilled_water_type_1

        chilled_water = _parse_chilled_water(d.pop("chilled_water"))

        update_emission_factors_dto = cls(
            electricity=electricity,
            gas=gas,
            steam=steam,
            chilled_water=chilled_water,
        )

        update_emission_factors_dto.additional_properties = d
        return update_emission_factors_dto

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
