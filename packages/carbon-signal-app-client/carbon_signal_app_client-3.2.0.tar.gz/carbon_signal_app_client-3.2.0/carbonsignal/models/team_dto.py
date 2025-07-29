from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TeamDTO")


@_attrs_define
class TeamDTO:
    """Create and edit team DTO.

    Attributes:
        name (str):
        avatar_id (Union[None, UUID]):
    """

    name: str
    avatar_id: None | UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        avatar_id: None | str
        avatar_id = str(self.avatar_id) if isinstance(self.avatar_id, UUID) else self.avatar_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "avatar_id": avatar_id,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_avatar_id(data: object) -> None | UUID:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                avatar_id_type_0 = UUID(data)

                return avatar_id_type_0
            except:  # noqa: E722
                pass
            return cast(None | UUID, data)

        avatar_id = _parse_avatar_id(d.pop("avatar_id"))

        team_dto = cls(
            name=name,
            avatar_id=avatar_id,
        )

        team_dto.additional_properties = d
        return team_dto

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
