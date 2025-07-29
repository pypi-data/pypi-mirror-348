from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.baseline_energy_not_complete_status import (
    BaselineEnergyNotCompleteStatus,
    check_baseline_energy_not_complete_status,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="BaselineEnergyNotComplete")


@_attrs_define
class BaselineEnergyNotComplete:
    """Represents a state where baseline energy is not yet complete or not started.

    Note: Ignore the "BaseModel" object. This is only returned for documentation purposes until the following bug report
    is fixed: https://github.com/scalar/scalar/issues/4590

        Attributes:
            status (BaselineEnergyNotCompleteStatus): Energy status.

                **Allowed values:**

                - `PROCESSING`
                - `QUEUED`
                - `FAILED`
            result (Union[Unset, None]):
            end_use (Union[Unset, None]):
    """

    status: BaselineEnergyNotCompleteStatus
    result: Unset | None = UNSET
    end_use: Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status: str = self.status

        result = self.result

        end_use = self.end_use

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
        })
        if result is not UNSET:
            field_dict["result"] = result
        if end_use is not UNSET:
            field_dict["end_use"] = end_use

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = check_baseline_energy_not_complete_status(d.pop("status"))

        result = d.pop("result", UNSET)

        end_use = d.pop("end_use", UNSET)

        baseline_energy_not_complete = cls(
            status=status,
            result=result,
            end_use=end_use,
        )

        baseline_energy_not_complete.additional_properties = d
        return baseline_energy_not_complete

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
