from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_building_role_role import UserBuildingRoleRole, check_user_building_role_role

if TYPE_CHECKING:
    from ..models.public_user import PublicUser


T = TypeVar("T", bound="UserBuildingRole")


@_attrs_define
class UserBuildingRole:
    """Building guest model.

    Attributes:
        id (int):
        building_id (int):
        role (UserBuildingRoleRole):
        user (PublicUser): Public user.

            This object contains "public" attributes, excluding private user details such as settings etc..
    """

    id: int
    building_id: int
    role: UserBuildingRoleRole
    user: "PublicUser"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        building_id = self.building_id

        role: str = self.role

        user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "building_id": building_id,
            "role": role,
            "user": user,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.public_user import PublicUser

        d = dict(src_dict)
        id = d.pop("id")

        building_id = d.pop("building_id")

        role = check_user_building_role_role(d.pop("role"))

        user = PublicUser.from_dict(d.pop("user"))

        user_building_role = cls(
            id=id,
            building_id=building_id,
            role=role,
            user=user,
        )

        user_building_role.additional_properties = d
        return user_building_role

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
