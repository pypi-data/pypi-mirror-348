from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_team_role_dto_role import UpdateTeamRoleDTORole, check_update_team_role_dto_role

T = TypeVar("T", bound="UpdateTeamRoleDTO")


@_attrs_define
class UpdateTeamRoleDTO:
    """Update team role DTO.

    Attributes:
        role (UpdateTeamRoleDTORole):
    """

    role: UpdateTeamRoleDTORole
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role: str = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "role": role,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = check_update_team_role_dto_role(d.pop("role"))

        update_team_role_dto = cls(
            role=role,
        )

        update_team_role_dto.additional_properties = d
        return update_team_role_dto

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
