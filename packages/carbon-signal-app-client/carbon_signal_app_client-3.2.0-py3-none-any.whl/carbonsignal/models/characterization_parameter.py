from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.characterization_statistic import CharacterizationStatistic


T = TypeVar("T", bound="CharacterizationParameter")


@_attrs_define
class CharacterizationParameter:
    """CharacterizationParameter.

    Represents a building characterization parameter with its design space and actual values.

        Attributes:
            id (str): Parameter ID
            name (str): Characterization name
            description (str): Description of the parameter
            label (str): Unit of measurement
            ticks (list[str]): Tick values of the design space
            values (CharacterizationStatistic): CharacterizationStatistic.

                This provides the statistics for a specific design space.
    """

    id: str
    name: str
    description: str
    label: str
    ticks: list[str]
    values: "CharacterizationStatistic"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        label = self.label

        ticks = self.ticks

        values = self.values.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "description": description,
            "label": label,
            "ticks": ticks,
            "values": values,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.characterization_statistic import CharacterizationStatistic

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        label = d.pop("label")

        ticks = cast(list[str], d.pop("ticks"))

        values = CharacterizationStatistic.from_dict(d.pop("values"))

        characterization_parameter = cls(
            id=id,
            name=name,
            description=description,
            label=label,
            ticks=ticks,
            values=values,
        )

        characterization_parameter.additional_properties = d
        return characterization_parameter

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
