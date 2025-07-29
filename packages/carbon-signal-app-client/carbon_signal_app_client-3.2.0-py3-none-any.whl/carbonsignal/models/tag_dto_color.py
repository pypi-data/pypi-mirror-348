from typing import Literal, cast

TagDTOColor = Literal[
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

TAG_DTO_COLOR_VALUES: set[TagDTOColor] = {
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


def check_tag_dto_color(value: str) -> TagDTOColor:
    if value in TAG_DTO_COLOR_VALUES:
        return cast(TagDTOColor, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {TAG_DTO_COLOR_VALUES!r}")
