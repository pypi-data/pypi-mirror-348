from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.timeline_intervention_complete import TimelineInterventionComplete
    from ..models.timeline_intervention_not_complete import TimelineInterventionNotComplete


T = TypeVar("T", bound="BuildingTimelineItem")


@_attrs_define
class BuildingTimelineItem:
    """BuildingTimelineItem.

    Attributes:
        intervention (Union['TimelineInterventionComplete', 'TimelineInterventionNotComplete']):
        year (int):
        intervention_ids (list[int]):
    """

    intervention: Union["TimelineInterventionComplete", "TimelineInterventionNotComplete"]
    year: int
    intervention_ids: list[int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.timeline_intervention_not_complete import TimelineInterventionNotComplete

        intervention: dict[str, Any]
        if isinstance(self.intervention, TimelineInterventionNotComplete):
            intervention = self.intervention.to_dict()
        else:
            intervention = self.intervention.to_dict()

        year = self.year

        intervention_ids = self.intervention_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "intervention": intervention,
            "year": year,
            "intervention_ids": intervention_ids,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.timeline_intervention_complete import TimelineInterventionComplete
        from ..models.timeline_intervention_not_complete import TimelineInterventionNotComplete

        d = dict(src_dict)

        def _parse_intervention(
            data: object,
        ) -> Union["TimelineInterventionComplete", "TimelineInterventionNotComplete"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                intervention_type_0 = TimelineInterventionNotComplete.from_dict(data)

                return intervention_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            intervention_type_1 = TimelineInterventionComplete.from_dict(data)

            return intervention_type_1

        intervention = _parse_intervention(d.pop("intervention"))

        year = d.pop("year")

        intervention_ids = cast(list[int], d.pop("intervention_ids"))

        building_timeline_item = cls(
            intervention=intervention,
            year=year,
            intervention_ids=intervention_ids,
        )

        building_timeline_item.additional_properties = d
        return building_timeline_item

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
