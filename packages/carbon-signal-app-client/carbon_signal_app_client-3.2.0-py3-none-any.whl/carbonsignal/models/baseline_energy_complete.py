from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.building_energy_result_meters import BuildingEnergyResultMeters
    from ..models.end_use import EndUse


T = TypeVar("T", bound="BaselineEnergyComplete")


@_attrs_define
class BaselineEnergyComplete:
    """BaselineEnergyComplete.

    Represents a state where the baseline model is complete, and the baseline energy is also complete.
    This means the baseline is fully generated.

        Attributes:
            status (Literal['COMPLETED']):
            result (BuildingEnergyResultMeters): BuildingEnergyResultMeters.
            end_use (EndUse): End use model.
    """

    status: Literal["COMPLETED"]
    result: "BuildingEnergyResultMeters"
    end_use: "EndUse"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status

        result = self.result.to_dict()

        end_use = self.end_use.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
            "result": result,
            "end_use": end_use,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.building_energy_result_meters import BuildingEnergyResultMeters
        from ..models.end_use import EndUse

        d = dict(src_dict)
        status = cast(Literal["COMPLETED"], d.pop("status"))
        if status != "COMPLETED":
            raise ValueError(f"status must match const 'COMPLETED', got '{status}'")

        result = BuildingEnergyResultMeters.from_dict(d.pop("result"))

        end_use = EndUse.from_dict(d.pop("end_use"))

        baseline_energy_complete = cls(
            status=status,
            result=result,
            end_use=end_use,
        )

        baseline_energy_complete.additional_properties = d
        return baseline_energy_complete

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
