from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.baseline_characterization_not_complete_status import (
    BaselineCharacterizationNotCompleteStatus,
    check_baseline_characterization_not_complete_status,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="BaselineCharacterizationNotComplete")


@_attrs_define
class BaselineCharacterizationNotComplete:
    """BaselineCharacterizationNotComplete.

    Represents a state where the baseline model is not yet complete.

        Attributes:
            status (BaselineCharacterizationNotCompleteStatus):
            result (Union[Unset, None]):
            design_space (Union[Unset, None]):
    """

    status: BaselineCharacterizationNotCompleteStatus
    result: Unset | None = UNSET
    design_space: Unset | None = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status: str = self.status

        result = self.result

        design_space = self.design_space

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
        })
        if result is not UNSET:
            field_dict["result"] = result
        if design_space is not UNSET:
            field_dict["design_space"] = design_space

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = check_baseline_characterization_not_complete_status(d.pop("status"))

        result = d.pop("result", UNSET)

        design_space = d.pop("design_space", UNSET)

        baseline_characterization_not_complete = cls(
            status=status,
            result=result,
            design_space=design_space,
        )

        baseline_characterization_not_complete.additional_properties = d
        return baseline_characterization_not_complete

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
