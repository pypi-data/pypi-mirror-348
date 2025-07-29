import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.team_credit_type import TeamCreditType, check_team_credit_type

T = TypeVar("T", bound="TeamCredit")


@_attrs_define
class TeamCredit:
    """Team credit usage schema.

    Attributes:
        id (int):
        type_ (TeamCreditType):
        date (datetime.datetime):
    """

    id: int
    type_: TeamCreditType
    date: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: str = self.type_

        date = self.date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "type": type_,
            "date": date,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_team_credit_type(d.pop("type"))

        date = isoparse(d.pop("date"))

        team_credit = cls(
            id=id,
            type_=type_,
            date=date,
        )

        team_credit.additional_properties = d
        return team_credit

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
