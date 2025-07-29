from typing import Literal, cast

UpdateTeamTagBulkDTOColor = Literal[
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

UPDATE_TEAM_TAG_BULK_DTO_COLOR_VALUES: set[UpdateTeamTagBulkDTOColor] = {
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


def check_update_team_tag_bulk_dto_color(value: str) -> UpdateTeamTagBulkDTOColor:
    if value in UPDATE_TEAM_TAG_BULK_DTO_COLOR_VALUES:
        return cast(UpdateTeamTagBulkDTOColor, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {UPDATE_TEAM_TAG_BULK_DTO_COLOR_VALUES!r}")
