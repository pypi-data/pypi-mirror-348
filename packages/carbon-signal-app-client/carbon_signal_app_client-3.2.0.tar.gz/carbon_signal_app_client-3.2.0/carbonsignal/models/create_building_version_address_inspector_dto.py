from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateBuildingVersionAddressInspectorDTO")


@_attrs_define
class CreateBuildingVersionAddressInspectorDTO:
    """CreateBuildingVersionAddressDTOInspect.

    Attributes:
        type_ (Literal['ADDRESS']):
        address (Union[None, str]):
        city (Union[None, str]):
        state (Union[None, str]):
        zip_ (Union[None, str]):
        country (Union[None, str]):
    """

    type_: Literal["ADDRESS"]
    address: None | str
    city: None | str
    state: None | str
    zip_: None | str
    country: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        address: None | str
        address = self.address

        city: None | str
        city = self.city

        state: None | str
        state = self.state

        zip_: None | str
        zip_ = self.zip_

        country: None | str
        country = self.country

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "address": address,
            "city": city,
            "state": state,
            "zip": zip_,
            "country": country,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = cast(Literal["ADDRESS"], d.pop("type"))
        if type_ != "ADDRESS":
            raise ValueError(f"type must match const 'ADDRESS', got '{type_}'")

        def _parse_address(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        address = _parse_address(d.pop("address"))

        def _parse_city(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        city = _parse_city(d.pop("city"))

        def _parse_state(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        state = _parse_state(d.pop("state"))

        def _parse_zip_(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        zip_ = _parse_zip_(d.pop("zip"))

        def _parse_country(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        country = _parse_country(d.pop("country"))

        create_building_version_address_inspector_dto = cls(
            type_=type_,
            address=address,
            city=city,
            state=state,
            zip_=zip_,
            country=country,
        )

        create_building_version_address_inspector_dto.additional_properties = d
        return create_building_version_address_inspector_dto

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
