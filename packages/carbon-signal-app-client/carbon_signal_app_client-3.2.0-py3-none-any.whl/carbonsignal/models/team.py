from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.avatar import Avatar
    from ..models.user_team_role import UserTeamRole


T = TypeVar("T", bound="Team")


@_attrs_define
class Team:
    """Team schema.

    Attributes:
        id (int):
        name (str):
        avatar (Union['Avatar', None]):
        roles (list['UserTeamRole']):
    """

    id: int
    name: str
    avatar: Union["Avatar", None]
    roles: list["UserTeamRole"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.avatar import Avatar

        id = self.id

        name = self.name

        avatar: None | dict[str, Any]
        avatar = self.avatar.to_dict() if isinstance(self.avatar, Avatar) else self.avatar

        roles = []
        for roles_item_data in self.roles:
            roles_item = roles_item_data.to_dict()
            roles.append(roles_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "avatar": avatar,
            "roles": roles,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.avatar import Avatar
        from ..models.user_team_role import UserTeamRole

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_avatar(data: object) -> Union["Avatar", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                avatar_type_0 = Avatar.from_dict(data)

                return avatar_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Avatar", None], data)

        avatar = _parse_avatar(d.pop("avatar"))

        roles = []
        _roles = d.pop("roles")
        for roles_item_data in _roles:
            roles_item = UserTeamRole.from_dict(roles_item_data)

            roles.append(roles_item)

        team = cls(
            id=id,
            name=name,
            avatar=avatar,
            roles=roles,
        )

        team.additional_properties = d
        return team

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
