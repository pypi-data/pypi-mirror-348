"""Test Config data class.

Config:
    # Required config settings:

    # API tokens
    lunatask_api_token: str
    todoist_api_token: str

    todoist_default_area: UUID

    # Optional config settings.

    # Task mapping
    todoist_project_map: dict[str, UUID | str] = field(default_factory=dict)

    todoist_task_source: str = "Todoist"
    todoist_task_include_source_id: bool = False
    todoist_collaborator_relationship = "business-contacts"
    todoist_label_reminder: str = "Create Goals for Todoist Labels"
    todoist_priority: dict[str, int] = field(
        default_factory=lambda: {"p1": 2, "p2": 1, "p3": 0, "p4": -1}
    )
    todoist_deadline_format: str = "[Deadline: {deadline_date}]"
    todoist_deadline_date_only_format: str = "%Y-%m-%d"
    todoist_deadline_date_time_format: str = "%Y-%m-%d %H:%M:%S"
"""

# ruff: noqa: D103, S101

import uuid
from typing import Final

import dataclass_wizard.errors
import pytest

import config
from lunatask.models.people import Relationship

# Gross!
TEST_LUNATASK_API_TOKEN: Final[str] = (
    config.LUNTASK_API_TOKEN_VALID
    * (config.LUNATASK_API_TOKEN_LENGTH // len(config.LUNTASK_API_TOKEN_VALID) + 1)
)[:600]
TEST_TODOIST_API_TOKEN: Final[str] = "deadbeef" * 5
TEST_UUID: Final[uuid.UUID] = uuid.uuid3(uuid.NAMESPACE_URL, "test")

TEST_PROJECT_MAP: Final[dict[str, uuid.UUID]] = {
    "Example - 🏡 Project 1": TEST_UUID,
    "Example - Project 2 💡": TEST_UUID,
    "Example - 🧹 Chores": TEST_UUID,
}

TEST_PRIORITY_MAP: Final[dict[str, int]] = {
    "p1": 2,
    "p2": 1,
    "p3": 0,
    "p4": -1,
}


def test_config_full() -> None:
    test_config = config.Config.from_toml_file("tests/data/test_config_full.toml")

    assert test_config.lunatask_api_token == TEST_LUNATASK_API_TOKEN
    assert test_config.todoist_api_token == TEST_TODOIST_API_TOKEN
    assert test_config.todoist_default_area == TEST_UUID

    assert len(test_config.todoist_project_map) == len(TEST_PROJECT_MAP)
    for k in TEST_PROJECT_MAP:
        assert test_config.todoist_project_map[k] == TEST_PROJECT_MAP[k]
    assert test_config.todoist_task_source == "Todoist"
    assert test_config.todoist_task_include_source_id
    assert (
        test_config.todoist_collaborator_relationship == Relationship.BUSINESS_CONTACTS
    )
    assert test_config.todoist_label_reminder == "Create Goals for Todoist Labels"
    assert test_config.todoist_recurring_reminder == "Update recurring tasks"
    assert test_config.todoist_deadline_format == "[Deadline: {deadline_date}]"
    assert test_config.todoist_deadline_date_only_format == "%Y-%m-%d"
    assert test_config.todoist_deadline_date_time_format == "%Y-%m-%d %H:%M:%S"
    assert len(test_config.todoist_priority) == len(TEST_PRIORITY_MAP)
    for k in TEST_PRIORITY_MAP:
        assert test_config.todoist_priority[k] == TEST_PRIORITY_MAP[k]


def test_config_partial() -> None:
    test_config = config.Config.from_toml_file("tests/data/test_config_partial.toml")

    assert test_config.lunatask_api_token == TEST_LUNATASK_API_TOKEN
    assert test_config.todoist_api_token == TEST_TODOIST_API_TOKEN
    assert test_config.todoist_default_area == TEST_UUID

    assert len(test_config.todoist_project_map) == 0
    assert test_config.todoist_task_source == "Todoist"
    assert not test_config.todoist_task_include_source_id
    assert (
        test_config.todoist_collaborator_relationship == Relationship.BUSINESS_CONTACTS
    )
    assert test_config.todoist_label_reminder == "Create Goals for Todoist Labels"
    assert test_config.todoist_recurring_reminder == "Update recurring tasks"
    assert test_config.todoist_deadline_format == "[Deadline: {deadline_date}]"
    assert test_config.todoist_deadline_date_only_format == "%Y-%m-%d"
    assert test_config.todoist_deadline_date_time_format == "%Y-%m-%d %H:%M:%S"
    assert len(test_config.todoist_priority) == len(TEST_PRIORITY_MAP)
    for k in TEST_PRIORITY_MAP:
        assert test_config.todoist_priority[k] == TEST_PRIORITY_MAP[k]


def test_config_default() -> None:
    # Invalid API token, so that's as far as we get.
    with pytest.raises(ValueError):  # noqa: PT011
        _ = config.Config.from_toml_file("todoist2lunatask.config.template")


def test_config_empty() -> None:
    with pytest.raises(dataclass_wizard.errors.MissingFields):
        _ = config.Config.from_toml_file("tests/data/test_config_empty.toml")


def test_config_no_file() -> None:
    with pytest.raises(OSError):  # noqa: PT011
        _ = config.Config.from_toml_file("tests/data/NoFileExistsHere.toml")


def test_config_invalid_area() -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        _ = config.Config.from_toml_file("tests/data/test_config_invalid_area.toml")


def test_config_invalid_relationship() -> None:
    test_config = config.Config.from_toml_file(
        "tests/data/test_config_invalid_relationship.toml"
    )
    assert (
        test_config.todoist_collaborator_relationship == Relationship.BUSINESS_CONTACTS
    )


def test_config_invalid_token_length() -> None:
    with pytest.raises(config.TokenLengthError):
        _ = config.Config.from_toml_file(
            "tests/data/test_config_invalid_api_token_length.toml"
        )

    with pytest.raises(config.TokenLengthError):
        _ = config.Config.from_toml_file(
            "tests/data/test_config_invalid_api_token_length2.toml"
        )


def test_config_invalid_token_chars() -> None:
    with pytest.raises(config.TokenInvalidCharacterError):
        _ = config.Config.from_toml_file(
            "tests/data/test_config_invalid_api_token_chars.toml"
        )

    with pytest.raises(config.TokenInvalidCharacterError):
        _ = config.Config.from_toml_file(
            "tests/data/test_config_invalid_api_token_chars2.toml"
        )
