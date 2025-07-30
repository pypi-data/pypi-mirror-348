"""Configuration file object."""

import string
from dataclasses import dataclass, field
from typing import Annotated, Final, Self
from uuid import UUID

from dataclass_wizard import KeyPath, TOMLWizard

from lunatask.models.people import Relationship

# Current API tokens are expected to be:
#
# - Todoist: 40 characters, hex
# - Lunatask: 600 characters, [A-Za-z0-9._]
#
# Lunatask's token seems to be split into three fields by the "." characters.
# Not sure about the encoding.
LUNATASK_API_TOKEN_LENGTH: Final[int] = 600
TODOIST_API_TOKEN_LENGTH: Final[int] = 40

LUNTASK_API_TOKEN_VALID: Final[str] = (
    ".-_" + string.ascii_uppercase + string.ascii_lowercase + string.digits
)
TODOIST_API_TOKEN_VALID: Final[str] = string.hexdigits


class TokenLengthError(ValueError):
    """The API token has an invalid length."""


class TokenInvalidCharacterError(ValueError):
    """The API token has invalid characters."""


@dataclass
class Config(TOMLWizard):
    """todoist2lunatask configuration.

    You *MUST* supply API tokens and a default area ID, everything else is
    optional. See the todoist2lunatask.config.template for examples and
    detailed docs.
    """

    # Required config settings:

    # API tokens
    lunatask_api_token: str
    todoist_api_token: str

    todoist_default_area: UUID

    # Optional config settings.

    # Task mapping
    todoist_project_map: dict[str, UUID] = field(default_factory=dict)

    todoist_task_source: Annotated[str, KeyPath("optional.todoist_task_source")] = (
        "Todoist"
    )
    todoist_task_include_source_id: Annotated[
        bool, KeyPath("optional.todoist_task_include_source_id")
    ] = False
    todoist_collaborator_relationship: Annotated[
        str | Relationship, KeyPath("optional.todoist_collaborator_relationship")
    ] = Relationship.BUSINESS_CONTACTS
    todoist_label_reminder: Annotated[
        str, KeyPath("optional.todoist_label_reminder")
    ] = "Create Goals for Todoist Labels"
    todoist_recurring_reminder: Annotated[
        str, KeyPath("optional.todoist_recurring_reminder")
    ] = "Update recurring tasks"

    todoist_deadline_format: Annotated[
        str, KeyPath("optional.todoist_deadline_format")
    ] = "[Deadline: {deadline_date}]"
    todoist_deadline_date_only_format: Annotated[
        str, KeyPath("optional.todoist_deadline_date_only_format")
    ] = "%Y-%m-%d"
    todoist_deadline_date_time_format: Annotated[
        str, KeyPath("optional.todoist_deadline_date_time_format")
    ] = "%Y-%m-%d %H:%M:%S"

    todoist_priority: dict[str, int] = field(
        default_factory=lambda: {"p1": 2, "p2": 1, "p3": 0, "p4": -1}
    )

    def __post_init__(self: Self) -> None:
        """Check API tokens."""
        if len(self.todoist_api_token) != TODOIST_API_TOKEN_LENGTH:
            raise TokenLengthError

        if len(self.lunatask_api_token) != LUNATASK_API_TOKEN_LENGTH:
            raise TokenLengthError

        for c in self.todoist_api_token:
            if c not in TODOIST_API_TOKEN_VALID:
                raise TokenInvalidCharacterError

        for c in self.lunatask_api_token:
            if c not in LUNTASK_API_TOKEN_VALID:
                raise TokenInvalidCharacterError

        # Convert todoist_collaborator_relationship if necessary.
        if self.todoist_collaborator_relationship not in Relationship:
            # Invalid value, use the default.
            self.todoist_collaborator_relationship = Relationship.BUSINESS_CONTACTS
        elif isinstance(self.todoist_collaborator_relationship, str):
            self.todoist_collaborator_relationship = Relationship(
                self.todoist_collaborator_relationship
            )
