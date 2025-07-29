from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.worker_version_dto import WorkerVersionDTO


T = TypeVar("T", bound="VersionResponseDTO")


@_attrs_define
class VersionResponseDTO:
    """Version response DTO.

    Attributes:
        api (Union[None, str]):
        workers (list['WorkerVersionDTO']):
    """

    api: None | str
    workers: list["WorkerVersionDTO"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        api: None | str
        api = self.api

        workers = []
        for workers_item_data in self.workers:
            workers_item = workers_item_data.to_dict()
            workers.append(workers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "api": api,
            "workers": workers,
        })

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.worker_version_dto import WorkerVersionDTO

        d = dict(src_dict)

        def _parse_api(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        api = _parse_api(d.pop("api"))

        workers = []
        _workers = d.pop("workers")
        for workers_item_data in _workers:
            workers_item = WorkerVersionDTO.from_dict(workers_item_data)

            workers.append(workers_item)

        version_response_dto = cls(
            api=api,
            workers=workers,
        )

        version_response_dto.additional_properties = d
        return version_response_dto

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
