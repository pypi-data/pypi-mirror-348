from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.building_timeline_item import BuildingTimelineItem


T = TypeVar("T", bound="BuildingTimeline")


@_attrs_define
class BuildingTimeline:
    """BuildingTimeline.

    Attributes:
        building_id (int):
        timeline (list['BuildingTimelineItem']):
    """

    building_id: int
    timeline: list["BuildingTimelineItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        building_id = self.building_id

        timeline = []
        for timeline_item_data in self.timeline:
            timeline_item = timeline_item_data.to_dict()
            timeline.append(timeline_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "building_id": building_id,
            "timeline": timeline,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.building_timeline_item import BuildingTimelineItem

        d = dict(src_dict)
        building_id = d.pop("building_id")

        timeline = []
        _timeline = d.pop("timeline")
        for timeline_item_data in _timeline:
            timeline_item = BuildingTimelineItem.from_dict(timeline_item_data)

            timeline.append(timeline_item)

        building_timeline = cls(
            building_id=building_id,
            timeline=timeline,
        )

        building_timeline.additional_properties = d
        return building_timeline

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
