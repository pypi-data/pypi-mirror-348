from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="LocationCoordinates")


@_attrs_define
class LocationCoordinates:
    """LocationCoordinates.

    Attributes:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        type_ (Literal['COORDINATES']):
    """

    lat: float
    lon: float
    type_: Literal["COORDINATES"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        lat = self.lat

        lon = self.lon

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "lat": lat,
            "lon": lon,
            "type": type_,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lat = d.pop("lat")

        lon = d.pop("lon")

        type_ = cast(Literal["COORDINATES"], d.pop("type"))
        if type_ != "COORDINATES":
            raise ValueError(f"type must match const 'COORDINATES', got '{type_}'")

        location_coordinates = cls(
            lat=lat,
            lon=lon,
            type_=type_,
        )

        location_coordinates.additional_properties = d
        return location_coordinates

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
