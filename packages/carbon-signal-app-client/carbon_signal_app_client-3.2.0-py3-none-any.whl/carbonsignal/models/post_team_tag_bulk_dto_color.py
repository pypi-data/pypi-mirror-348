from typing import Literal, cast

PostTeamTagBulkDTOColor = Literal[
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

POST_TEAM_TAG_BULK_DTO_COLOR_VALUES: set[PostTeamTagBulkDTOColor] = {
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


def check_post_team_tag_bulk_dto_color(value: str) -> PostTeamTagBulkDTOColor:
    if value in POST_TEAM_TAG_BULK_DTO_COLOR_VALUES:
        return cast(PostTeamTagBulkDTOColor, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {POST_TEAM_TAG_BULK_DTO_COLOR_VALUES!r}")
