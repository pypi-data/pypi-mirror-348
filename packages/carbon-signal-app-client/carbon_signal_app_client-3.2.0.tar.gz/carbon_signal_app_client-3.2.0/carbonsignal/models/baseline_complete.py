from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.baseline_characterization_complete import BaselineCharacterizationComplete
    from ..models.baseline_energy_complete import BaselineEnergyComplete


T = TypeVar("T", bound="BaselineComplete")


@_attrs_define
class BaselineComplete:
    """BaselineComplete.

    Both characterization and baseline energy are complete.

        Attributes:
            characterization (BaselineCharacterizationComplete): BaselineCharacterizationComplete.

                Represents a state where the baseline characterization is complete.
            energy (BaselineEnergyComplete): BaselineEnergyComplete.

                Represents a state where the baseline model is complete, and the baseline energy is also complete.
                This means the baseline is fully generated.
    """

    characterization: "BaselineCharacterizationComplete"
    energy: "BaselineEnergyComplete"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        characterization = self.characterization.to_dict()

        energy = self.energy.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "characterization": characterization,
            "energy": energy,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.baseline_characterization_complete import BaselineCharacterizationComplete
        from ..models.baseline_energy_complete import BaselineEnergyComplete

        d = dict(src_dict)
        characterization = BaselineCharacterizationComplete.from_dict(d.pop("characterization"))

        energy = BaselineEnergyComplete.from_dict(d.pop("energy"))

        baseline_complete = cls(
            characterization=characterization,
            energy=energy,
        )

        baseline_complete.additional_properties = d
        return baseline_complete

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
