from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.public_user import PublicUser


T = TypeVar("T", bound="InviteToken")


@_attrs_define
class InviteToken:
    """Invite token schema.

    Attributes:
        id (str):
        user_id (int):
        user (PublicUser): Public user.

            This object contains "public" attributes, excluding private user details such as settings etc..
    """

    id: str
    user_id: int
    user: "PublicUser"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        user_id = self.user_id

        user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "user_id": user_id,
            "user": user,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.public_user import PublicUser

        d = dict(src_dict)
        id = d.pop("id")

        user_id = d.pop("user_id")

        user = PublicUser.from_dict(d.pop("user"))

        invite_token = cls(
            id=id,
            user_id=user_id,
            user=user,
        )

        invite_token.additional_properties = d
        return invite_token

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
