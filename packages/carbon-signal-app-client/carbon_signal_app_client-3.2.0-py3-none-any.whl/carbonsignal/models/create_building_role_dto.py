from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_building_role_dto_role import CreateBuildingRoleDTORole, check_create_building_role_dto_role

T = TypeVar("T", bound="CreateBuildingRoleDTO")


@_attrs_define
class CreateBuildingRoleDTO:
    """Create building role DTO.

    Attributes:
        email (str):
        role (CreateBuildingRoleDTORole):
    """

    email: str
    role: CreateBuildingRoleDTORole
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        role: str = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "email": email,
            "role": role,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        role = check_create_building_role_dto_role(d.pop("role"))

        create_building_role_dto = cls(
            email=email,
            role=role,
        )

        create_building_role_dto.additional_properties = d
        return create_building_role_dto

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
