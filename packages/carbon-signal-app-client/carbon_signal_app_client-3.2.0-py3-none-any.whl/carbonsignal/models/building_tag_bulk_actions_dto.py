from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.building_tag_bulk_dto import BuildingTagBulkDTO


T = TypeVar("T", bound="BuildingTagBulkActionsDTO")


@_attrs_define
class BuildingTagBulkActionsDTO:
    """Bulk building tag actions DTO.

    Attributes:
        actions (list['BuildingTagBulkDTO']):
    """

    actions: list["BuildingTagBulkDTO"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()
            actions.append(actions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "actions": actions,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.building_tag_bulk_dto import BuildingTagBulkDTO

        d = dict(src_dict)
        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = BuildingTagBulkDTO.from_dict(actions_item_data)

            actions.append(actions_item)

        building_tag_bulk_actions_dto = cls(
            actions=actions,
        )

        building_tag_bulk_actions_dto.additional_properties = d
        return building_tag_bulk_actions_dto

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
