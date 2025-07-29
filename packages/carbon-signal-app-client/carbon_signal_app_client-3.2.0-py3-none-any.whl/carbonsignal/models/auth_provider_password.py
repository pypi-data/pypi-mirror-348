from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthProviderPassword")


@_attrs_define
class AuthProviderPassword:
    """Response model for password provider.

    Attributes:
        provider (Union[Literal['PASSWORD'], Unset]):  Default: 'PASSWORD'.
    """

    provider: Literal["PASSWORD"] | Unset = "PASSWORD"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if provider is not UNSET:
            field_dict["provider"] = provider

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider = cast(Literal["PASSWORD"] | Unset, d.pop("provider", UNSET))
        if provider != "PASSWORD" and not isinstance(provider, Unset):
            raise ValueError(f"provider must match const 'PASSWORD', got '{provider}'")

        auth_provider_password = cls(
            provider=provider,
        )

        auth_provider_password.additional_properties = d
        return auth_provider_password

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
