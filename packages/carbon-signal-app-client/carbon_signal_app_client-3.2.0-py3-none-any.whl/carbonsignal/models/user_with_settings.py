from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.avatar import Avatar
    from ..models.user_settings import UserSettings


T = TypeVar("T", bound="UserWithSettings")


@_attrs_define
class UserWithSettings:
    """UserWithSettings.

    The user object with nested user settings.

        Attributes:
            id (int):
            name (Union[None, str]):
            email (str):
            avatar (Union['Avatar', None]):
            settings (UserSettings): User settings.

                These attributes are used to store user preferences that adjust different aspects of the dashboard.<br/>
                These attributes don't affect anything else within other API endpoints, such as returned unit types, etc.
    """

    id: int
    name: None | str
    email: str
    avatar: Union["Avatar", None]
    settings: "UserSettings"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.avatar import Avatar

        id = self.id

        name: None | str
        name = self.name

        email = self.email

        avatar: None | dict[str, Any]
        avatar = self.avatar.to_dict() if isinstance(self.avatar, Avatar) else self.avatar

        settings = self.settings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "email": email,
            "avatar": avatar,
            "settings": settings,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.avatar import Avatar
        from ..models.user_settings import UserSettings

        d = dict(src_dict)
        id = d.pop("id")

        def _parse_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        name = _parse_name(d.pop("name"))

        email = d.pop("email")

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

        settings = UserSettings.from_dict(d.pop("settings"))

        user_with_settings = cls(
            id=id,
            name=name,
            email=email,
            avatar=avatar,
            settings=settings,
        )

        user_with_settings.additional_properties = d
        return user_with_settings

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
