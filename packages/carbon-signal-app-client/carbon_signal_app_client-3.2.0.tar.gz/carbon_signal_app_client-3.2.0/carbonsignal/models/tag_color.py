from typing import Literal, cast

TagColor = Literal[
    "brand",
    "cyan",
    "error",
    "fuchsia",
    "gray",
    "gray-blue",
    "green-light",
    "orange-dark",
    "rose",
    "success",
    "teal",
    "violet",
    "warning",
    "yellow",
]

TAG_COLOR_VALUES: set[TagColor] = {
    "brand",
    "cyan",
    "error",
    "fuchsia",
    "gray",
    "gray-blue",
    "green-light",
    "orange-dark",
    "rose",
    "success",
    "teal",
    "violet",
    "warning",
    "yellow",
}


def check_tag_color(value: str) -> TagColor:
    if value in TAG_COLOR_VALUES:
        return cast(TagColor, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TAG_COLOR_VALUES!r}")
