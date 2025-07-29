from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_team_role_role_type_0 import UserTeamRoleRoleType0, check_user_team_role_role_type_0

if TYPE_CHECKING:
    from ..models.public_user import PublicUser


T = TypeVar("T", bound="UserTeamRole")


@_attrs_define
class UserTeamRole:
    """User team member schema.

    Attributes:
        id (int):
        role (Union[Literal['GUEST'], UserTeamRoleRoleType0]):
        user (PublicUser): Public user.

            This object contains "public" attributes, excluding private user details such as settings etc..
    """

    id: int
    role: Literal["GUEST"] | UserTeamRoleRoleType0
    user: "PublicUser"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        role: Literal["GUEST"] | str
        role = self.role if isinstance(self.role, str) else self.role

        user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "role": role,
            "user": user,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.public_user import PublicUser

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_role(data: object) -> Literal["GUEST"] | UserTeamRoleRoleType0:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_0 = check_user_team_role_role_type_0(data)

                return role_type_0
            except:  # noqa: E722
                pass
            role_type_1 = cast(Literal["GUEST"], data)
            if role_type_1 != "GUEST":
                raise ValueError(f"role_type_1 must match const 'GUEST', got '{role_type_1}'")
            return role_type_1

        role = _parse_role(d.pop("role"))

        user = PublicUser.from_dict(d.pop("user"))

        user_team_role = cls(
            id=id,
            role=role,
            user=user,
        )

        user_team_role.additional_properties = d
        return user_team_role

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
