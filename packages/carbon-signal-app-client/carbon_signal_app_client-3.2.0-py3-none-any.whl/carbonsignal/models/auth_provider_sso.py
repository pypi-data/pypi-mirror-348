from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sso_provider import SSOProvider


T = TypeVar("T", bound="AuthProviderSSO")


@_attrs_define
class AuthProviderSSO:
    """Response model for SSO provider.

    Attributes:
        sso_provider (SSOProvider): SSO provider model.
        provider (Union[Literal['SSO'], Unset]):  Default: 'SSO'.
    """

    sso_provider: "SSOProvider"
    provider: Literal["SSO"] | Unset = "SSO"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sso_provider = self.sso_provider.to_dict()

        provider = self.provider

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "sso_provider": sso_provider,
        })
        if provider is not UNSET:
            field_dict["provider"] = provider

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.sso_provider import SSOProvider

        d = dict(src_dict)
        sso_provider = SSOProvider.from_dict(d.pop("sso_provider"))

        provider = cast(Literal["SSO"] | Unset, d.pop("provider", UNSET))
        if provider != "SSO" and not isinstance(provider, Unset):
            raise ValueError(f"provider must match const 'SSO', got '{provider}'")

        auth_provider_sso = cls(
            sso_provider=sso_provider,
            provider=provider,
        )

        auth_provider_sso.additional_properties = d
        return auth_provider_sso

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
