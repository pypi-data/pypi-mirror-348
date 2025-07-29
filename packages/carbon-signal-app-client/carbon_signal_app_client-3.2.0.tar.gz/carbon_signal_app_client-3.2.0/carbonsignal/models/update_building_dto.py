from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.update_emission_factors_dto import UpdateEmissionFactorsDTO


T = TypeVar("T", bound="UpdateBuildingDTO")


@_attrs_define
class UpdateBuildingDTO:
    """Update building DTO.

    Attributes:
        name (str): Name of the building.
        emission_factors (UpdateEmissionFactorsDTO): UpdateEmissionFactors.
        notes (Union[None, str]):
        is_gap_filling_allowed (bool):
    """

    name: str
    emission_factors: "UpdateEmissionFactorsDTO"
    notes: None | str
    is_gap_filling_allowed: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        emission_factors = self.emission_factors.to_dict()

        notes: None | str
        notes = self.notes

        is_gap_filling_allowed = self.is_gap_filling_allowed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "emission_factors": emission_factors,
            "notes": notes,
            "is_gap_filling_allowed": is_gap_filling_allowed,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_emission_factors_dto import UpdateEmissionFactorsDTO

        d = dict(src_dict)
        name = d.pop("name")

        emission_factors = UpdateEmissionFactorsDTO.from_dict(d.pop("emission_factors"))

        def _parse_notes(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        notes = _parse_notes(d.pop("notes"))

        is_gap_filling_allowed = d.pop("is_gap_filling_allowed")

        update_building_dto = cls(
            name=name,
            emission_factors=emission_factors,
            notes=notes,
            is_gap_filling_allowed=is_gap_filling_allowed,
        )

        update_building_dto.additional_properties = d
        return update_building_dto

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
