from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.base_model import BaseModel
    from ..models.baseline_characterization_complete import BaselineCharacterizationComplete
    from ..models.baseline_energy_not_complete import BaselineEnergyNotComplete


T = TypeVar("T", bound="BaselineEnergyRunning")


@_attrs_define
class BaselineEnergyRunning:
    """BaselineEnergyRunning.

    Characterization is complete, but baseline energy is still running.

        Attributes:
            characterization (BaselineCharacterizationComplete): BaselineCharacterizationComplete.

                Represents a state where the baseline characterization is complete.
            energy (Union['BaseModel', 'BaselineEnergyNotComplete', None]): Baseline energy generation status.
    """

    characterization: "BaselineCharacterizationComplete"
    energy: Union["BaseModel", "BaselineEnergyNotComplete", None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_model import BaseModel
        from ..models.baseline_energy_not_complete import BaselineEnergyNotComplete

        characterization = self.characterization.to_dict()

        energy: None | dict[str, Any]
        if isinstance(self.energy, BaselineEnergyNotComplete | BaseModel):
            energy = self.energy.to_dict()
        else:
            energy = self.energy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "characterization": characterization,
            "energy": energy,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_model import BaseModel
        from ..models.baseline_characterization_complete import BaselineCharacterizationComplete
        from ..models.baseline_energy_not_complete import BaselineEnergyNotComplete

        d = dict(src_dict)
        characterization = BaselineCharacterizationComplete.from_dict(d.pop("characterization"))

        def _parse_energy(data: object) -> Union["BaseModel", "BaselineEnergyNotComplete", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                energy_type_0 = BaselineEnergyNotComplete.from_dict(data)

                return energy_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                energy_type_1 = BaseModel.from_dict(data)

                return energy_type_1
            except:  # noqa: E722
                pass
            return cast(Union["BaseModel", "BaselineEnergyNotComplete", None], data)

        energy = _parse_energy(d.pop("energy"))

        baseline_energy_running = cls(
            characterization=characterization,
            energy=energy,
        )

        baseline_energy_running.additional_properties = d
        return baseline_energy_running

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
