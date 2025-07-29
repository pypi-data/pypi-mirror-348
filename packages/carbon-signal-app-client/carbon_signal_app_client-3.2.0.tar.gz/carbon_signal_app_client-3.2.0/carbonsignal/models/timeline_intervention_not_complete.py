from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.timeline_intervention_not_complete_status_type_0 import (
    TimelineInterventionNotCompleteStatusType0,
    check_timeline_intervention_not_complete_status_type_0,
)

T = TypeVar("T", bound="TimelineInterventionNotComplete")


@_attrs_define
class TimelineInterventionNotComplete:
    """Timeline InterventionNotComplete.

    Attributes:
        emissions (None):
        energy (None):
        status (Union[None, TimelineInterventionNotCompleteStatusType0]): Status of the intervention.

            **Allowed values:**

            - `PROCESSING`
            - `QUEUED`
            - `FAILED`
            - `null` *(represents that the intervention has not started and is likely waiting to be queued)*
    """

    emissions: None
    energy: None
    status: None | TimelineInterventionNotCompleteStatusType0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        emissions = self.emissions

        energy = self.energy

        status: None | str
        status = self.status if isinstance(self.status, str) else self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "emissions": emissions,
            "energy": energy,
            "status": status,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        emissions = d.pop("emissions")

        energy = d.pop("energy")

        def _parse_status(data: object) -> None | TimelineInterventionNotCompleteStatusType0:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = check_timeline_intervention_not_complete_status_type_0(data)

                return status_type_0
            except:  # noqa: E722
                pass
            return cast(None | TimelineInterventionNotCompleteStatusType0, data)

        status = _parse_status(d.pop("status"))

        timeline_intervention_not_complete = cls(
            emissions=emissions,
            energy=energy,
            status=status,
        )

        timeline_intervention_not_complete.additional_properties = d
        return timeline_intervention_not_complete

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
