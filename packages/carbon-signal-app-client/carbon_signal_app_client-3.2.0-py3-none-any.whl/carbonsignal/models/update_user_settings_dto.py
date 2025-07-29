from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_user_settings_dto_display_unit import (
    UpdateUserSettingsDTODisplayUnit,
    check_update_user_settings_dto_display_unit,
)

T = TypeVar("T", bound="UpdateUserSettingsDTO")


@_attrs_define
class UpdateUserSettingsDTO:
    """Update model for UserSettings.

    Attributes:
        display_unit (UpdateUserSettingsDTODisplayUnit): Preferred display unit.

            **Note:** the value of this attribute does not change the units returned through the API. This only adjusts the
            units displayed in the UI at app.carbonsignal.com.
        active_team_id (Union[None, int]): Currently active team ID. Use this ID for other API endpoints that require a
            `team_id` input parameter.
    """

    display_unit: UpdateUserSettingsDTODisplayUnit
    active_team_id: None | int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_unit: str = self.display_unit

        active_team_id: None | int
        active_team_id = self.active_team_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "display_unit": display_unit,
            "active_team_id": active_team_id,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        display_unit = check_update_user_settings_dto_display_unit(d.pop("display_unit"))

        def _parse_active_team_id(data: object) -> None | int:
            if data is None:
                return data
            return cast(None | int, data)

        active_team_id = _parse_active_team_id(d.pop("active_team_id"))

        update_user_settings_dto = cls(
            display_unit=display_unit,
            active_team_id=active_team_id,
        )

        update_user_settings_dto.additional_properties = d
        return update_user_settings_dto

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
