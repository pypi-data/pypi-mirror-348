from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.baseline_characterization_not_complete import BaselineCharacterizationNotComplete


T = TypeVar("T", bound="BaselineCharacterizationRunning")


@_attrs_define
class BaselineCharacterizationRunning:
    """BaselineCharacterizationRunning.

    Characterization is still running, so baseline energy has not started.

        Attributes:
            characterization (BaselineCharacterizationNotComplete): BaselineCharacterizationNotComplete.

                Represents a state where the baseline model is not yet complete.
            energy (Union[Unset, None]):
    """

    characterization: "BaselineCharacterizationNotComplete"
    energy: Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        characterization = self.characterization.to_dict()

        energy = self.energy

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "characterization": characterization,
        })
        if energy is not UNSET:
            field_dict["energy"] = energy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.baseline_characterization_not_complete import BaselineCharacterizationNotComplete

        d = dict(src_dict)
        characterization = BaselineCharacterizationNotComplete.from_dict(d.pop("characterization"))

        energy = d.pop("energy", UNSET)

        baseline_characterization_running = cls(
            characterization=characterization,
            energy=energy,
        )

        baseline_characterization_running.additional_properties = d
        return baseline_characterization_running

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
