from typing import Literal, cast

EmissionFactorSource = Literal["CUSTOM", "DEFAULT"]

EMISSION_FACTOR_SOURCE_VALUES: set[EmissionFactorSource] = {
    "CUSTOM",
    "DEFAULT",
}


def check_emission_factor_source(value: str) -> EmissionFactorSource:
    if value in EMISSION_FACTOR_SOURCE_VALUES:
        return cast(EmissionFactorSource, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {EMISSION_FACTOR_SOURCE_VALUES!r}")
