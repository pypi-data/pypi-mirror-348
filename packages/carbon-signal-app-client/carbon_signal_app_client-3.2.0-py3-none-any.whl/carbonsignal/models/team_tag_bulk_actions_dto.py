from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.delete_team_tag_bulk_dto import DeleteTeamTagBulkDTO
    from ..models.post_team_tag_bulk_dto import PostTeamTagBulkDTO
    from ..models.update_team_tag_bulk_dto import UpdateTeamTagBulkDTO


T = TypeVar("T", bound="TeamTagBulkActionsDTO")


@_attrs_define
class TeamTagBulkActionsDTO:
    """Bulk team tag actions DTO.

    Attributes:
        actions (list[Union['DeleteTeamTagBulkDTO', 'PostTeamTagBulkDTO', 'UpdateTeamTagBulkDTO']]):
    """

    actions: list[Union["DeleteTeamTagBulkDTO", "PostTeamTagBulkDTO", "UpdateTeamTagBulkDTO"]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.post_team_tag_bulk_dto import PostTeamTagBulkDTO
        from ..models.update_team_tag_bulk_dto import UpdateTeamTagBulkDTO

        actions = []
        for actions_item_data in self.actions:
            actions_item: dict[str, Any]
            if isinstance(actions_item_data, PostTeamTagBulkDTO | UpdateTeamTagBulkDTO):
                actions_item = actions_item_data.to_dict()
            else:
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
        from ..models.delete_team_tag_bulk_dto import DeleteTeamTagBulkDTO
        from ..models.post_team_tag_bulk_dto import PostTeamTagBulkDTO
        from ..models.update_team_tag_bulk_dto import UpdateTeamTagBulkDTO

        d = dict(src_dict)
        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:

            def _parse_actions_item(
                data: object,
            ) -> Union["DeleteTeamTagBulkDTO", "PostTeamTagBulkDTO", "UpdateTeamTagBulkDTO"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    actions_item_type_0 = PostTeamTagBulkDTO.from_dict(data)

                    return actions_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    actions_item_type_1 = UpdateTeamTagBulkDTO.from_dict(data)

                    return actions_item_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                actions_item_type_2 = DeleteTeamTagBulkDTO.from_dict(data)

                return actions_item_type_2

            actions_item = _parse_actions_item(actions_item_data)

            actions.append(actions_item)

        team_tag_bulk_actions_dto = cls(
            actions=actions,
        )

        team_tag_bulk_actions_dto.additional_properties = d
        return team_tag_bulk_actions_dto

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
