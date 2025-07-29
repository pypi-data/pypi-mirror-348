from typing import Literal, cast

BuildingTagBulkDTOAction = Literal["DELETE", "POST"]

BUILDING_TAG_BULK_DTO_ACTION_VALUES: set[BuildingTagBulkDTOAction] = {
    "DELETE",
    "POST",
}


def check_building_tag_bulk_dto_action(value: str) -> BuildingTagBulkDTOAction:
    if value in BUILDING_TAG_BULK_DTO_ACTION_VALUES:
        return cast(BuildingTagBulkDTOAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {BUILDING_TAG_BULK_DTO_ACTION_VALUES!r}")
