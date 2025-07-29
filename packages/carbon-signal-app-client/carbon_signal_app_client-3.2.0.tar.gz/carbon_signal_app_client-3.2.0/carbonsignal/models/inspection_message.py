from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.inspection_type import InspectionType, check_inspection_type
from ..types import UNSET, Unset

T = TypeVar("T", bound="InspectionMessage")


@_attrs_define
class InspectionMessage:
    """
    Attributes:
        message (str):
        type_ (Union[Unset, InspectionType]): Validation message types.
    """

    message: str
    type_: Unset | InspectionType = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        type_: Unset | str = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "message": message,
        })
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        _type_ = d.pop("type", UNSET)
        type_: Unset | InspectionType
        type_ = UNSET if isinstance(_type_, Unset) else check_inspection_type(_type_)

        inspection_message = cls(
            message=message,
            type_=type_,
        )

        inspection_message.additional_properties = d
        return inspection_message

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
